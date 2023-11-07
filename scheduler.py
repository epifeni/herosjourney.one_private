import schedule
import time
import os
from datetime import datetime, timedelta

# Import your Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartlearning.settings")

def run_management_command():
    # Run the management command
    os.system("python manage.py update_free_credits")

# Calculate the next month's date and time
now = datetime.now()
next_month = now.replace(day=1) + timedelta(days=32 - now.day)
next_month = next_month.replace(hour=0, minute=0, second=0, microsecond=0)

# Schedule the management command to run at the start of each month
schedule.every().day.at(next_month.strftime("%H:%M")).do(run_management_command)

while True:
    schedule.run_pending()
    time.sleep(1)
