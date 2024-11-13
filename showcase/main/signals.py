# main/signals.py
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(user_signed_up)
def create_user_profile_on_signup(request, user, **kwargs):
    # Ensure the user profile is created if it doesn’t already exist
    UserProfile.objects.get_or_create(user=user)
