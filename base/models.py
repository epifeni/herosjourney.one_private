from django.db import models
from datetime import datetime
from custom_accounts.models import  User

class Course(models.Model):
    CATEGORY_CHOICES = (
        ('computer-science', 'Computer Science'),
        ('data-science', 'Data science'),
        ('engineering', 'Engineering'),
        ('web-development', 'Web Development'),
        ('architecture', 'Architecture'),
        # Add more choices as needed
    )
    SUB_CATEGORY_CHOICES = (
        ('ml', 'Machine Learning'),
        ('data_science', 'Data Science'),
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('php', 'PHP'),
        ('django', 'Django'),
        ('html', 'HTML'),
        ('reactjs', 'React JS'),
        ('front-end', 'Front-End'),
        ('back-end', 'Back-End'),

        # Add more choices as needed
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 50 , null = False)
    slug = models.CharField(max_length = 50 , null = False , unique = True)
    description = models.TextField( null = True)
    price = models.IntegerField(null=False,default = 0, blank=True)
    discount = models.IntegerField(null=False ,blank=True, default = 0) 

    active = models.BooleanField(default = False)
    
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default='',  blank=True)
    sub_category = models.CharField(max_length=255, choices=SUB_CATEGORY_CHOICES, default='', null=True, blank=True)
    thumbnail = models.ImageField(upload_to = "files/thumbnail") 
    date = models.DateTimeField(auto_now_add= True) 
    resource = models.FileField(upload_to = "files/resource", blank=True, null=True)
    length = models.IntegerField(null=False)

    instructor_name = models.CharField(max_length=50, null=True)
    enroll_now_status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CourseProperty(models.Model):
    description  = models.CharField(max_length = 300 , null = False)
    course = models.ForeignKey(Course , null = False , on_delete=models.CASCADE)

    class Meta : 
        abstract = True


class Tag(CourseProperty):
    pass
    
class Prerequisite(CourseProperty):
    pass

class Learning(CourseProperty):
    pass


class Video(models.Model):
    title  = models.CharField(max_length = 100 , null = False)
    course = models.ForeignKey(Course , null = False , on_delete=models.CASCADE)
    serial_number = models.IntegerField(null=False)
    video_id = models.CharField(max_length = 100 , null = False)
    is_preview = models.BooleanField(default = False)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # OneToOneField instead of ForeignKey
    course = models.ManyToManyField(Course ,  blank=True)
    date = models.DateTimeField(auto_now_add=True)

    credits = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    free_credits = models.DecimalField(max_digits=8, decimal_places=2, default=18000)  # 5 hours in seconds


    def deduct_credits(self, duration):
        # Deduct purchased credits first
        if self.credits >= duration:
            self.credits -= duration
        else:
            remaining_duration = duration - self.credits
            self.credits = 0
            # Deduct remaining duration from free credits
            if self.free_credits >= remaining_duration:
                self.free_credits -= remaining_duration
            else:
                self.free_credits = 0

        self.save()

    def start_of_month(self):
        # Ensure that self.date is not None before accessing its attributes
        if self.date is not None:
            now = datetime.now()
            start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            if now >= start_of_month:
                # Check if it's the start of the month or a new month has started
                if self.date.month != now.month:
                    # Reset free_credits to 18000 (5 hours) at the start of the new month
                    self.free_credits = 18000
                    self.date = now  # Update the last update date
                    self.save()
        else:
            # Handle the case where self.date is None (e.g., not set during registration)
            pass

    def save(self, *args, **kwargs):
        # Call the start_of_month method before saving the object
        self.start_of_month()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)





