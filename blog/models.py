from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(default=timezone.now)
    commentaire = models.CharField(max_length=200, default='')
    image = models.ImageField(upload_to='articles_images/', blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)

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