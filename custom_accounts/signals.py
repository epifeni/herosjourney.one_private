from django.db.models.signals import post_save
from django.dispatch import receiver
from custom_accounts.models import User
from base.models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
