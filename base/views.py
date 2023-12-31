from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages , auth
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model, authenticate, login, logout
from custom_accounts.models import  User
from base.models import  Course, Video, UserProfile
from base.serializers import (List_accounts_Serializer,User_profile_Serializer)
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from custom_accounts.forms import UserForm, MyUserCreationForm, EditProfileForm

from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.utils import timezone
from datetime import timedelta


#Views Function here

User = get_user_model()

#Home page
def home(request):
    categories = Course.CATEGORY_CHOICES  # Get all category choices from the model
    category_id = request.GET.get('category')  # Get the selected category from the query parameters
    if category_id:
        courses = Course.objects.filter(category=category_id)  # Filter courses based on the selected category
    else:
        courses = Course.objects.all()
    return render(request, 'base/index.html', {'courses': courses, 'categories': categories})


#Course Details
def courses(request):
    categories = Course.CATEGORY_CHOICES  # Get all category choices from the model
    category_id = request.GET.get('category')  # Get the selected category from the query parameters
    query = request.GET.get('q')  # Get the search query from the query parameters

    if category_id:
        courses = Course.objects.filter(category=category_id)  # Filter courses based on the selected category
    else:
        courses = Course.objects.all()

    if query:
        # Search by course name, title, and tags using Q objects
        courses = courses.filter(
            Q(name__icontains=query) |  # Search in course names
            Q(slug__icontains=query) |  # Search in course titles
            Q(description__icontains=query)  # Search in course tags
        )

    return render(request, 'base/course.html', {'courses': courses, 'categories': categories})

def EnrollCource(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.user.is_authenticated:
        # Get or create user profile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        if request.method == 'POST':
            if course not in user_profile.course.all():
                user_profile.course.add(course)  # Add the course to the user's enrolled courses
            messages.success(request, "You have successfully enrolled in this course.")
            # return redirect('course-detail', slug=slug)  # Redirect to course detail page
        
        is_enrolled = user_profile.course.filter(slug=slug).exists()
        return render(request, 'base/enrollnow.html', {'course': course, 'is_enrolled': is_enrolled})
    else:
        return render(request, 'base/enrollnow.html', {'course': course})


@login_required
def coursePage(request, slug):
    if request.user.is_authenticated:
        course = get_object_or_404(Course, slug=slug)
        user_profile = UserProfile.objects.get(user=request.user)
        videos = course.video_set.all().order_by('serial_number')

        serial_number = request.GET.get('lecture')
        try:
            video = Video.objects.get(serial_number=serial_number, course=course)
        except ObjectDoesNotExist:
            # Handle the case when the video does not exist
            # For example, you can redirect the user to a different page
            return HttpResponse("Video not found.", status=404)
                                
        video = Video.objects.get(serial_number=serial_number, course=course)

        credit_balance = user_profile.credits
        remaining_free_credits = user_profile.free_credits

        return render(request, 'base/course_page.html', {'videos':videos,'course': course, 'video':video, 'remaining_free_credits': remaining_free_credits, 'credit_balance': credit_balance})
    else:
        return redirect('login')


@csrf_exempt
@login_required
def deduct_credits(request):
    if request.method == 'POST':
        duration = int(request.POST.get('duration'))
        print('Duration Played (in seconds):', duration)
        
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)

            # Deduct purchased credits first
            remaining_credits = user_profile.credits - duration
            
            if remaining_credits >= 0:
                user_profile.credits = remaining_credits
            else:
                remaining_duration = duration - user_profile.credits
                user_profile.credits = 0
                user_profile.free_credits = max(0, user_profile.free_credits - remaining_duration)

            user_profile.save()

            print('Remaining Purchased Credits:', user_profile.credits)
            print('Remaining Free Credits:', user_profile.free_credits)

            return JsonResponse({
                'credit_balance': user_profile.credits,
                'remaining_free_credits': user_profile.free_credits,
            })

        else:
            return JsonResponse({
                'error': 'User is not authenticated',
            }, status=401)

    else:
        return JsonResponse({
            'error': 'Invalid request method',
        }, status=405)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def update_credit(request):
    now = timezone.now()
    start_of_month = now.replace(day=1)

    profile_list = UserProfile.objects.all().order_by('-id')
    for i in profile_list:
        if now.date().day - start_of_month.date().day == 0:
            i.free_credits = 18000
            i.date = start_of_month  # Set the date to the start of the current month
            i.save()
        else:
            pass
    get_data = User_profile_Serializer(profile_list, many=True)
    if request.method == "GET":
        return Response(get_data.data)

def aboutUs(request):
    return render(request, 'base/about.html')

def contactUs(request):
    return render(request, 'base/contact.html')

def donateNow(request):
    return render(request, 'base/donate.html')

