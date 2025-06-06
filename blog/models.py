from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.timezone import now
from django.urls import reverse

class Tag(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True)
    icone = models.ImageField(upload_to='categories_icons/', blank=True, null=True)

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('categorie_detail', kwargs={'slug': self.slug})

class Article(models.Model):
    STATUT_CHOICES = [
            ('brouillon', 'Brouillon'),
            ('publie', 'Publié'),
            ('archive', 'Archivé'),
        ]
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(default=timezone.now)
    commentaire = models.CharField(max_length=200, default='')
    image = models.ImageField(upload_to='articles_images/', blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='brouillon')

    def __str__(self):
        return self.titre

    class Meta:
        ordering = ['-date_creation']

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('lecteur', 'Lecteur'),
        ('auteur', 'Auteur'),
        ('editeur', 'Éditeur'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='lecteur')

    def __str__(self):
        return self.username

class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auteur} - {self.article}"


class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(default=now)
    user_agent = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.path} - {self.timestamp}"

class ArticleLike(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('article', 'user')