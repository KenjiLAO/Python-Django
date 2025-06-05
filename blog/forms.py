from django import forms
from .models import Article, Commentaire , Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class ArticleForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Étiquettes"
    )

    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'commentaire', 'categorie', 'image', 'tags']
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder': 'Titre de l\'article'}),
            'contenu': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Contenu'}),
            'commentaire': forms.TextInput(attrs={'placeholder': 'Commentaire'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'tags': forms.SelectMultiple(attrs={'size': 5}),
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