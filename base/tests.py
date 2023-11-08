# base/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from base.models import UserProfile
from base.signals import monthly_update_credits


class UserProfileTest(TestCase):
    def test_monthly_update_credits(self):
        user = User.objects.get(username="maxxi2")  # Retrieve the user
        self.assertTrue(user.check_password("karachi12"))  # Verify the user's password

        initial_credits = self.user_profile.credits
        monthly_update_credits.send(sender=None)
        self.user_profile.refresh_from_db()
        updated_credits = self.user_profile.credits

        self.assertTrue(updated_credits > initial_credits)

