from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
import logging

logger = logging.getLogger('app')

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info(f"Utilisateur connecté : {user.username} (id={user.id})")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    logger.info(f"Utilisateur déconnecté : {user.username} (id={user.id})")
