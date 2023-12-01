"""

http://sls.com:8000/social-auth/complete/google-oauth2



Django settings for smartlearning project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from pathlib import Path
from decouple import config
import os
# from social_core.backends.authbroker import AuthBrokerJSONResponse

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
# config_path = os.path.join(BASE_DIR, '.env')
# config.read_file(open(config_path))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'SECRET_KEY_2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = [ ]

CSRF_TRUSTED_ORIGINS = [
    'https://herosjourneyoneprivate-production.up.railway.app',
    # 'http://www.herosjourney.one',
    'https://www.herosjourney.one',
    'https://herosjourney.one',
    'https://web-production-fe22.up.railway.app'
]

SITE_ID = 1

# Application definition
INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',

#run this in a new enviroment if the current has been misplaced. 'python manage.py crontab add'
    'django_crontab',

    # 'whitenoise.runserver_nostatic', 

    'custom_accounts', # custom_users_accounts app
    'payments', # custom_payments app
    'base', # main django app
    
    'social_django', # social-auth-app-django library

    

    #'checkout', # stripe app
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    ##################################################
    ########## middleware for social_django ##########
    ##################################################
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'smartlearning.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                ##################################################
                ###### context_processors for social_django ######
                ##################################################
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'smartlearning.wsgi.application'
AUTH_USER_MODEL = 'custom_accounts.User'


CRONJOBS = [
    ('0 0 1 * *', 'base.models.send_monthly_update_credits')
]

# CRONJOBS = [

# ('* * * * *', 'base.models.send_monthly_update_credits')

# ]


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'Australia/Sydney'

TIME_ZONE = 'Pacific/Pago_Pago'

# TIME_ZONE = 'Asia/Karachi'


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"



#User Upload the contetns. images files
MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images/')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




########################################################
###### Additional configuration for social_django ######
########################################################

SIGNUP_REDIRECT_URL = 'login'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'login'

LOGOUT_REDIRECT_URL = 'login'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.twitter.TwitterOAuth', #for Twitter OAuth
    'social_core.backends.google.GoogleOAuth2', #for Google OAuth 2.0
]

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. In some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social_core.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social_core.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    'social_core.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social_core.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social_core.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social_core.pipeline.mail.mail_validation',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    'social_core.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social_core.pipeline.user.create_user',

    # Create the record that associates the social account with the user.
    'social_core.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social_core.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social_core.pipeline.user.user_details',
)

#Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY  = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET  = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

#Twitter
SOCIAL_AUTH_TWITTER_KEY = config('SOCIAL_AUTH_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = config('SOCIAL_AUTH_TWITTER_SECRET')
#SOCIAL_AUTH_TWITTER_CALLBACK = config('SOCIAL_AUTH_TWITTER_CALLBACK')


########################################################
##################### STRIPE KEYS ######################
########################################################
#ok
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'EMAIL_HOST_USER_OK'
EMAIL_HOST_PASSWORD = 'EMAIL_HOST_PASSWORD_OK'

#This is stripe key.

