from django.core.management.base import BaseCommand
from base.signals import monthly_update_credits
from base.models import UserProfile

class Command(BaseCommand):
    help = 'Update user free credits on the start of each month'

    def handle(self, *args, **options):
        monthly_update_credits.send(sender=None)
        self.stdout.write(self.style.SUCCESS('Updating Free Credits ......................... !! '))
        # Display information about user profiles
        user_profiles = UserProfile.objects.all()
        for user_profile in user_profiles:
            self.stdout.write(f'User: {user_profile.user}, Free Credits: {user_profile.free_credits}')

        self.stdout.write(self.style.SUCCESS('Successfully updated user credits for the start of the month.'))
