import logging
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from .models import Article, Categorie ,Tag, ArticleLike, Commentaire
from .forms import ArticleForm, CustomUserCreationForm, CommentaireForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator


logger = logging.getLogger('app')

def home(request):
    categorie_nom = request.GET.get('categorie')
    categories = Categorie.objects.all()

    if categorie_nom:
        article_list = Article.objects.filter(categorie__nom=categorie_nom)
    else:
        article_list = Article.objects.all()

    paginator = Paginator(article_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Nombre total d’articles (filtrés ou non)
    total_articles = article_list.count()

    return render(request, 'blog/home.html', {
        'page_obj': page_obj,
        'categories': categories,
        'categorie_selectionnee': categorie_nom,
        'total_articles': total_articles,
    })

@login_required
def ajouter_article(request):
    user_role = getattr(request.user, 'role_effectif', request.user.role)

    if not request.user.role_effectif in ['admin', 'editeur', 'auteur']:
        logger.warning(
                    f"Tentative d'accès non autorisée à l'ajout d'article par l'utilisateur '{request.user.username}' (role: {user_role})"
                )
        return redirect('unauthorized')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.auteur = request.user
            article.save()
            form.save_m2m()
            logger.info(f"Nouvel article ajouté : {article.titre} ")
            return redirect('home')
    else:
        form = ArticleForm()
    return render(request, 'blog/ajouter_article.html', {'form': form})


def detail_article(request, id):
    article = get_object_or_404(Article, pk=id)
    commentaires = article.commentaires.all().order_by('-date_creation')
    can_edit = request.user.is_authenticated and request.user.role in ['auteur', 'editeur', 'admin']

    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.auteur = request.user
            commentaire.article = article
            commentaire.save()
            return redirect('detail_article', id=article.id)
    else:
        form = CommentaireForm()

    return render(request, 'blog/detail_article.html', {
        'article': article,
        'commentaires': commentaires,
        'can_edit': can_edit,
        'form': form
    })


@login_required
def modifier_article(request, id):
    article = get_object_or_404(Article, id=id)

    if not (request.user.role == 'admin' or article.auteur == request.user):
        return HttpResponseForbidden("Vous n'avez pas la permission de modifier cet article.")

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article modifié avec succès.")
            return redirect('home')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/modifier_article.html', {'form': form})

@login_required
def supprimer_article(request, id):
    article = get_object_or_404(Article, id=id)

    if not (request.user.role == 'admin' or article.auteur == request.user):
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer cet article.")

    if request.method == 'POST':
        logger.warning(f"Article {article.id} supprimé par {request.user.username}")
        article.delete()
        messages.success(request, "Article supprimé.")
        return redirect('home')
    return render(request, 'blog/supprimer_article.html', {'article': article})


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde en base
            logger.info(f"Nouvel utilisateur inscrit : {user.username} (id={user.id})")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

def unauthorized_view(request):
    return render(request, 'blog/unauthorized.html', status=403)

@csrf_exempt
def track_duration_view(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body.decode('utf-8'))
            path = data.get('path')
            duration = float(data.get('duration', 0))
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            ip = request.META.get('REMOTE_ADDR')

            UserActivity.objects.create(
                user=request.user,
                path=path,
                method='GET',
                timestamp=now(),
                user_agent=user_agent,
                ip_address=ip,
                duration=round(duration, 2)
            )
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'unauthorized'}, status=401)

def tags_populaires_view(request):
    tags = Tag.objects.annotate(nb_articles=Count('articles')).order_by('-nb_articles')[:50]  # top 50
    return render(request, 'blog/tags_populaires.html', {'tags': tags})

@login_required
def like_article(request):
    if request.method == "POST":
        article_id = request.POST.get('article_id')
        user = request.user
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return JsonResponse({'error': 'Article not found'}, status=404)

        like, created = ArticleLike.objects.get_or_create(article=article, user=user)
        if created:
            print(f"Like créé pour article {article_id} et user {user}")
        else:
            print(f"Like déjà existant pour article {article_id} et user {user}")

        return JsonResponse({'likes': article.articlelike_set.count(), 'already_liked': not created})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def categorie_detail(request, slug):
    categorie = get_object_or_404(Categorie, slug=slug)
    articles = Article.objects.filter(categorie=categorie)

    return render(request, 'blog/categorie_detail.html', {
        'categorie': categorie,
        'articles': articles
    })

@login_required
def supprimer_commentaire(request, id):
    commentaire = get_object_or_404(Commentaire, id=id)

    if not (request.user == commentaire.auteur or request.user.is_superuser):
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer ce commentaire.")

    if request.method == 'POST':
        article_id = commentaire.article.id
        commentaire.delete()
        messages.success(request, "Commentaire supprimé.")
        return redirect('detail_article', id=article_id)

    return render(request, 'blog/supprimer_commentaire.html', {'commentaire': commentaire})