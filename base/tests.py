from django.test import TestCase, override_settings
from django.utils import timezone
from datetime import timedelta
from freezegun import freeze_time
from custom_accounts.models import User
from base.models import UserProfile
from base.signals import monthly_update_credits



class UserProfileTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Any one-time setup for the entire test case can go here

    def setUp(self):
        self.user = User.objects.create_user(
            email='maxxi12@gmail.com', username='maxxi12', password='karachi12'
        )
        self.user_profile, _ = UserProfile.objects.get_or_create(user=self.user)

    def test_monthly_update_credits(self):
        with freeze_time("2023-02-03"):  # Set a specific date for testing
            self.assertTrue(monthly_update_credits.has_listeners())

            initial_credits = self.user_profile.free_credits
            monthly_update_credits.send(sender=None)
            self.user_profile.refresh_from_db()
            updated_credits = self.user_profile.free_credits

            self.assertGreater(updated_credits, initial_credits, "Credits should be increased after monthly update")

    def test_start_of_month(self):
        with freeze_time("2024-03-01"):  # Set a specific date for testing
            self.user_profile.start_of_month()

            self.assertEqual(
                self.user_profile.free_credits,
                18000,
                "Free credits should be set to 18000 at the start of the month"
            )
