from django import forms
from .models import Article, Commentaire
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'commentaire', 'categorie', 'image']
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder': 'Titre de l\'article'}),
            'contenu': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Contenu'}),
            'commentaire': forms.TextInput(attrs={'placeholder': 'Commentaire'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['contenu']