

from pathlib import Path
# import environ
import os

BASE_DIR = Path(__file__).resolve().parent.parent


# env = environ.Env(
#     DEBUG=(bool, False)
# )


# environ.Env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.

TEMPLATES_DIR = os.path.join(BASE_DIR , 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = env('SECRET_KEY')
SECRET_KEY='django-insecure-gzf(u4qg80w047^c2@+nw(s&tb-ltde=sv1+7rqz3-0aid7w*('

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env('DEBUG')
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'accounts.CustomUserModel'
# Application definition

DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

 
]


CUSTOM_APPS = [
    'accounts',
    'home',
    'Email_Template',
    'products',
    'mptt',
    'crispy_forms',
]

THIRD_PARTY_APPS = []

INSTALLED_APPS = DEFAULT_APPS + CUSTOM_APPS 

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'accounts.middlewares.simple_middleware',
    # 'products.middlewares.auth.auth_middleware',
    
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
   
]

SITE_ID  = 8

ACCOUNT_EMAIL_VERIFICATION = 'none'

LOGIN_REDIRECT_URL  = 'login'


ROOT_URLCONF = 'ecomm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'products.context_processor.Cart_Count',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecomm.wsgi.application'

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'Eshop_Db',
#        'USER': 'postgres',
#        'PASSWORD':'root',
#        'HOST': 'localhost',
#        'PORT': '5432',
#    }
# }
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
USE_TZ = True

TIME_ZONE = 'UTC'
# TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

STATIC_DIR = os.path.join(BASE_DIR,'static')

STATICFILES_DIRS = [STATIC_DIR,]

# STATICFILES_DIR = {
#     os.path.join(BASE_DIR , "static")
# }


MEDIA_ROOT =  os.path.join(BASE_DIR, 'static') 
MEDIA_URL = '/media/'


'''
Email Sending Configuration .
'''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = "sohailbadeghar561@gmail.com"
EMAIL_HOST_PASSWORD = "zgqigddcshicekca"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



LOGIN_REDIRECT_URL ='homepage'
LOGOUT_REDIRECT_URL ='homepage'



# Key_ID = 'rzp_test_Kp5HG5F8Z5NfVj'
# Key_Secret = 'Ijlpqn73WjBvw8VJkw4EGTt4'
razorpay_key_id = 'rzp_test_tGeRzPBvdwllWI'
razorpay_Key_Secret = 'Ro7IdrUx7zZ8TiN3vin2jqcj'


CRISPY_TEMPLATE_PACK = 'bootstrap4'


# STRIPE_PUBLIC_KEY=env('STRIPE_PUBLIC_KEY')

# STRIPE_SECRET_KEY=env('STRIPE_SECRET_KEY')



STRIPE_PUBLIC_KEY='pk_test_51M1mbuSFugonKGo0CgdPjLZWQ55zqc3YXbp38ubhy65EFq8mizb16LRmrG8BoRnlu9tYTVhSGMyNDLps2004Iaju00O9fjDh1I'
STRIPE_SECRET_KEY='sk_test_51M1mbuSFugonKGo0EQP8eyZYiRacNSJtfZo2yKvYR7BSJ14WrO0QzLpaTEEFkk65ZlkOcP1P8CwDkDvZsunysmJq00zjUbbiQb'

STRIPE_WEBHOOK_SECRET=' whsec_8f8b452eb6d03ec277e422007a741dd30fa0b39e9458630f5fd4304f052e1711'


'''
sendgrid email sending configurations

'''
# #sendgrid Api key:
# # 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
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_BACKEND = "sendgrid_backend.SendgridBackend",
# SENDGRID_API_KEY='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',

# #Toggle sandbox mode (when running in DEBUG mode)
# SENDGRID_SANDBOX_MODE_IN_DEBUG=True

# # echo to stdout or any other file-like object that is passed to the backend via the stream kwarg.
# SENDGRID_ECHO_TO_STDOUT=True
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False



