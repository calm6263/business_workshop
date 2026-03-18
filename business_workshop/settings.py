import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# الإعدادات الأساسية والأمان
# ============================================
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-default-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://localhost,http://127.0.0.1').split(',')
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')
CORS_ALLOW_CREDENTIALS = True

# ============================================
# التطبيقات المثبتة
# ============================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'news',
    'press_center',
    'events',
    'applicants',
    'schedule',
    'staff',
    'projects',
    'single_window',
    'fta_journal',
    'partners',
    'research',
    'departments.apps.DepartmentsConfig',
    'about_academy',
    'contacts',
    'coworking',
    'consultations',
    'contact_form',
    'accounts',
    'dashboards',
    'education_info',
    'notifications.apps.NotificationsConfig',
    'patents',
]

# لا نستخدم WhiteNoise على الإطلاق

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

# ============================================
# Middleware
# ============================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# ============================================
# إعدادات القوالب
# ============================================
ROOT_URLCONF = 'business_workshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'business_workshop.wsgi.application'

# ============================================
# قاعدة البيانات - PostgreSQL
# ============================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'business_db'),
        'USER': os.environ.get('POSTGRES_USER', 'business_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'business_password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# ============================================
# المصادقة وكلمات المرور
# ============================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# ============================================
# الإعدادات الدولية
# ============================================
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# ============================================
# الملفات الثابتة والوسائط (الإعدادات الأهم)
# ============================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']      # المجلد الذي يحتوي على ملفاتك الثابتة (css, js, images)
STATIC_ROOT = BASE_DIR / 'staticfiles'        # المجلد الذي سيُستخدم للإنتاج (يجمع الملفات)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# لا نستخدم أي معالج خاص (StaticFilesStorage الافتراضي)
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

ALLOWED_VIDEO_EXTENSIONS = ['mp4', 'mov', 'avi', 'wmv']

# ============================================
# إعدادات الأمان الإضافية
# ============================================
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = 'Lax'

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'Lax'

SECURE_CONTENT_TYPE_NOSNIFF = True
X_CONTENT_TYPE_OPTIONS = 'nosniff'

# ============================================
# إعدادات الجلسات
# ============================================
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True

# ============================================
# الإعدادات المخصصة
# ============================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================
# التخزين المؤقت
# ============================================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

if DEBUG:
    INTERNAL_IPS = ['127.0.0.1', 'localhost']
    DEBUG_TOOLBAR_CONFIG = {'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '{levelname} {asctime} {module} {message}', 'style': '{'},
        'simple': {'format': '{levelname} {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'level': 'DEBUG' if DEBUG else 'INFO', 'class': 'logging.StreamHandler', 'formatter': 'simple'},
    },
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'INFO'},
        'business_workshop': {'handlers': ['console'], 'level': 'DEBUG' if DEBUG else 'INFO'},
    },
}