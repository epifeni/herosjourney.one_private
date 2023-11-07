# from django.core.management.base import BaseCommand
# from base.models import UserProfile  # Replace 'yourapp' with your actual app name

# class Command(BaseCommand):
#     help = 'Update free credits at the start of each month'

#     def handle(self, *args, **options):
#         profiles = UserProfile.objects.all()
#         for profile in profiles:
#             profile.start_of_month()
#             self.stdout.write(self.style.WARNING(f'Profile Updated: {profile}, Free Credits: {profile.free_credits}'))
#             profile.save()
#         self.stdout.write(self.style.SUCCESS('Free credits updated successfully.'))



