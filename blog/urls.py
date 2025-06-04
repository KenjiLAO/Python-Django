from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', views.home, name='home'),
    path('ajouter/', views.ajouter_article, name='ajouter_article'),
    path('detail/<int:id>/', views.detail_article, name='detail_article'),
    path('modifier/<int:id>/', views.modifier_article, name='modifier_article'),
    path('supprimer/<int:id>/', views.supprimer_article, name='supprimer_article'),
    path('unauthorized/', views.unauthorized_view, name='unauthorized'),
    path('track-duration/', views.track_duration_view, name='track-duration'),
    path('tags-populaires/', views.tags_populaires_view, name='tags_populaires_view'),
    path('like-article/', views.like_article, name='like_article'),

    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('mot-de-passe-oublie/', auth_views.PasswordResetView.as_view(template_name='blog/password_reset.html'), name='password_reset'),
    path('mot-de-passe-oublie/envoye/', auth_views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'), name='password_reset_done'),
    path('reinitialiser/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reinitialisation-terminee/', auth_views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'), name='password_reset_complete'),
]

