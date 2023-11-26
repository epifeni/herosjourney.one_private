from django.db.models.signals import Signal
from django.dispatch import receiver


monthly_update_credits = Signal()

@receiver(monthly_update_credits)
def update_monthly_credits(sender, **kwargs):
    from .models import UserProfile
    for user_profile in UserProfile.objects.all():
        user_profile.start_of_month()
        user_profile.save()
