from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mountains_roads.apps.MountainsRoadsConfig',
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

ROOT_URLCONF = 'vgoru.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'vgoru.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'uk'
TIME_ZONE = 'Europe/Kyiv'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'mountains_roads:routes-list'
LOGOUT_REDIRECT_URL = 'mountains_roads:home'
LOGIN_URL = 'mountains_roads:login'

# ---------------------------------------------------------------------------
# Безпека — активуйте в production (local.py перекриває їх для розробки)
# ---------------------------------------------------------------------------

# Забороняє JavaScript читати CSRF-cookie.
# Активувати в production: CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False

# Cookie сесії передаються лише через HTTPS.
# Активувати в production: SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = False

# CSRF-cookie передається лише через HTTPS.
# Активувати в production: CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = False

# HTTP Strict Transport Security — примусово HTTPS на N секунд.
# Активувати в production: SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_SECONDS = 0

# Захист від Clickjacking (X-Frame-Options: DENY).
# Вже активний через XFrameOptionsMiddleware. Значення за замовчуванням: 'DENY'
X_FRAME_OPTIONS = 'DENY'