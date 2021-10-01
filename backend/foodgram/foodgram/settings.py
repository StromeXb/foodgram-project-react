import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'rest_framework',
    'django_filters',
    'djoser',
    'users',
    'recipes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodgram.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'foodgram.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

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

AUTH_USER_MODEL = 'users.User'

DJOSER = {
    'SEND_ACTIVATION_EMAIL': False,
    'LOGIN_FIELD': 'email',
    'LOGOUT_ON_PASSWORD_CHANGE': True,
    "PERMISSIONS":
        {
            "activation": ["rest_framework.permissions.AllowAny"],
            "password_reset": ["rest_framework.permissions.AllowAny"],
            "password_reset_confirm": ["rest_framework.permissions.AllowAny"],
            "set_password": ["djoser.permissions.CurrentUserOrAdmin"],
            "username_reset": ["rest_framework.permissions.AllowAny"],
            "username_reset_confirm": ["rest_framework.permissions.AllowAny"],
            "set_username": ["djoser.permissions.CurrentUserOrAdmin"],
            "user_create": ["rest_framework.permissions.AllowAny"],
            "user_delete": ["djoser.permissions.CurrentUserOrAdmin"],
            "user": ["djoser.permissions.CurrentUserOrAdmin"],
            "user_list": ["rest_framework.permissions.AllowAny"],
            "token_create": ["rest_framework.permissions.AllowAny"],
            "token_destroy": ["rest_framework.permissions.IsAuthenticated"],
        },
    "SERIALIZERS":
        {
            "activation": "djoser.serializers.ActivationSerializer",
            "password_reset": "djoser.serializers.SendEmailResetSerializer",
            "password_reset_confirm": "djoser.serializers.PasswordResetConfirmSerializer",
            "password_reset_confirm_retype": "djoser.serializers.PasswordResetConfirmRetypeSerializer",
            "set_password": "djoser.serializers.SetPasswordSerializer",
            "set_password_retype": "djoser.serializers.SetPasswordRetypeSerializer",
            "set_username": "djoser.serializers.SetUsernameSerializer",
            "set_username_retype": "djoser.serializers.SetUsernameRetypeSerializer",
            "username_reset": "djoser.serializers.SendEmailResetSerializer",
            "username_reset_confirm": "djoser.serializers.UsernameResetConfirmSerializer",
            "username_reset_confirm_retype": "djoser.serializers.UsernameResetConfirmRetypeSerializer",
            "user_create": "users.serializers.UsersCreateSerializer",
            "user_create_password_retype": "djoser.serializers.UserCreatePasswordRetypeSerializer",
            "user_delete": "djoser.serializers.UserDeleteSerializer",
            "user": "users.serializers.UserSerializer",
            "current_user": "users.serializers.UserSerializer",
            "token": "djoser.serializers.TokenSerializer",
            "token_create": "djoser.serializers.TokenCreateSerializer",
        },
    "HIDE_USERS": False,
 }

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
