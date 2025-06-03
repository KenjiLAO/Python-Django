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

    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
]

