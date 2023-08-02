import os


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

SECRET_KEY = "fake_secret_key_to_run_tests"  # noqa: S105

IS_INTERACTIVE = "INTERACTIVE" in os.environ

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.users",
    "wagtail.admin",
    "wagtail",
    "taggit",
    "wagtailmarkdown",
    "testapp" if IS_INTERACTIVE else "tests.testapp",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
            ],
        },
    },
]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_ROOT = os.path.join(PROJECT_DIR, "static")
STATIC_URL = "/static/"

ROOT_URLCONF = "testapp.urls" if IS_INTERACTIVE else "tests.testapp.urls"

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ALLOWED_HOSTS = ["*"]

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

WAGTAIL_SITE_NAME = "Wagtail Markdown Test"
WAGTAILADMIN_BASE_URL = "http://localhost:8020/"
WAGTAILDOCS_SERVE_METHOD = "direct"

DEBUG = IS_INTERACTIVE
