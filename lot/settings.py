import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x(qh_+o-6yko=kx9%hwy4+%2n8f5t8d(f8m-8wo_(h-x)!9r%1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'djoser',
    'tracker',
    'my_user',
    'lots',
    'number',
    'rest_auth',
    'django.contrib.sites',
    'rest_auth.registration',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lot.wsgi.application'

AUTH_USER_MODEL = 'my_user.User'

CORS_ORIGIN_ALLOW_ALL = True
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=33333),
    'REFRESH_TOKEN_LIFETIME': timedelta(seconds=100000),
    'AUTH_HEADER_TYPES': ('JWT', 'Bearer'),
}

SOCIAL_AUTH_VK_OAUTH2_KEY = '7445060'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'B3T2dybmC4kNQbec4v7v'
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email', ]
SOCIAL_AUTH_VK_APP_USER_MODE = 2


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '756415446899-temcqakf8ib1sa9kdda9rvo7d4i85a4p.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'LhZ0U6lMgj5v-BQxsQnbONu-'


REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAdminUser',
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',

        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',           # django-oauth-toolkit >= 1.0.0
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    )
}


'''from oauth2_provider.models import get_application_model


def enforce_public(client_id):
    client = get_application_model().objects.get(client_id=client_id)
    return client.client_type == client.CLIENT_PUBLIC


OAUTH2_PROVIDER = {
    "PKCE_REQUIRED": enforce_public
}'''
'''
OAUTH2_PROVIDER = {
    # other OAUTH2 settings
    # 'PKCE_REQUIRED': 'enforce_public',
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore'
}'''
OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
    },

    'CLIENT_ID_GENERATOR_CLASS': 'oauth2_provider.generators.ClientIdGenerator',

}
PKCE_REQUIRED = True

AUTHENTICATION_BACKENDS = (
    # Others auth providers (e.g. Google, OpenId, etc)

    # VK OAuth2
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.google.GooglePlusAuth',
    'social_core.backends.google.GoogleOAuth2',

    # django-rest-framework-social-oauth2
    'rest_framework_social_oauth2.backends.DjangoOAuth2',

    # Django
    'django.contrib.auth.backends.ModelBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
