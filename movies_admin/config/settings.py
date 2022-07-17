import os
from pathlib import Path
from dotenv import load_dotenv
from split_settings.tools import include


load_dotenv()

include(
    'components/database.py',
    'components/installed_apps.py',
    'components/middleware.py',
    'components/tamplates.py',
    'components/auto_password_validators.py',
)

DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')

SECRET_KEY = os.environ.get('SECRET_KEY')

BASE_DIR = Path(__file__).resolve().parent.parent

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOCALE_PATHS = ['movies/locale']

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:8080", ]
