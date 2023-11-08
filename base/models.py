from django.db import models
# from datetime import datetime
from custom_accounts.models import  User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import logging
from django.utils import timezone
from datetime import timedelta
from multitimer import MultiTimer  # Import MultiTimer
# from .signals import monthly_update_credits




class Course(models.Model):
    CATEGORY_CHOICES = (
        ('computer-science', 'Computer Science'),
        ('data-science', 'Data science'),
        ('engineering', 'Engineering'),
        ('web-development', 'Web Development'),
        ('architecture', 'Architecture'),
        ('training', 'Training')
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
        ('running', 'Running'),
        ('gym', 'GYM'),

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course, blank=True)
    date = models.DateTimeField(auto_now=True)
    credits = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    free_credits = models.DecimalField(max_digits=8, decimal_places=2, default=18000)  # 5 hours in seconds


    def deduct_credits(self, duration):
        if self.credits >= duration:
            self.credits -= duration
        else:
            remaining_duration = duration - self.credits
            self.credits = 0
            if self.free_credits >= remaining_duration:
                self.free_credits -= remaining_duration
            else:
                self.free_credits = 0
        self.save()


    def start_of_month(self):
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        if self.date.date() != start_of_month.date():
            self.free_credits = 18000
            self.date = start_of_month  # Set the date to the start of the current month
        else:
            pass

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if is_new:
            self.start_of_month()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


