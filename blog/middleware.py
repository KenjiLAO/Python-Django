import logging
import time
from django.shortcuts import redirect
from django.urls import resolve
from blog.models import UserActivity
from django.utils.timezone import now

logger = logging.getLogger('app')

# Définition des règles d’accès par nom de vue
ACCESS_RULES = {
    'ajouter_article': ['editeur', 'admin'],
    'modifier_article': ['editeur', 'admin'],
    'supprimer_article': ['editeur', 'admin'],
}

def get_client_ip(request):
    """Retourne l'adresse IP du client."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.role_effectif = 'editeur'
        else:
            request.user.role_effectif = 'lecteur'

        response = self.get_response(request)
        return response

class ActivityTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()  # Temps de début

        response = self.get_response(request)

        if request.user.is_authenticated and not request.path.startswith('/admin/'):
            end_time = time.time()  # Temps de fin
            duration = round(end_time - start_time, 3)  # En secondes

            ip = get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')

            UserActivity.objects.create(
                user=request.user,
                path=request.path,
                method=request.method,
                timestamp=now(),
                user_agent=user_agent,
                ip_address=ip,
                duration=duration
            )

            logger.info(f"{request.user.username} a visité {request.path} en {duration}s via {request.method} depuis {ip}")

        return response