import logging
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from .models import Article, Categorie ,Tag
from .forms import ArticleForm, CustomUserCreationForm, CommentaireForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.db.models import Count

logger = logging.getLogger('app')

def home(request):
    categorie_nom = request.GET.get('categorie')
    categories = Categorie.objects.all()

    if categorie_nom:
        articles = Article.objects.filter(categorie__nom=categorie_nom)
    else:
        articles = Article.objects.all()

    return render(request, 'blog/home.html', {
        'articles': articles,
        'categories': categories,
        'categorie_selectionnee': categorie_nom,
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
