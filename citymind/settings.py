from pathlib import Path
import os
import dj_database_url

# 🧠 CityMind - Django Settings
# -----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Solo cargar dotenv en local (no en producción)
if os.environ.get("DJANGO_ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")

# 🔑 Seguridad
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# 📦 Aplicaciones instaladas
INSTALLED_APPS = [
    # Django base
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Terceros
    "rest_framework",                # ← Django REST Framework
    "rest_framework.authtoken",      # ← Tokens (opcional, útil para autenticación futura)

    # Apps locales
    "core",
    "api",
    "dashboard",
]

# ⚙️ Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Para servir estáticos en producción
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "citymind.urls"

# 🎨 Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],   # templates personalizados
        "APP_DIRS": True,                   # busca plantillas dentro de cada app (incluyendo DRF)
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "citymind.wsgi.application"

# 🗄️ Base de datos (PostgreSQL por defecto)
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv(
            "DATABASE_URL",
            "postgres://citymind_user:citymind_pass@localhost:5432/citymind"
        ),
        conn_max_age=600,
        ssl_require=os.getenv("DJANGO_ENV") == "production"
    )
}

# 🔐 Validadores de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# 🌍 Internacionalización
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# 📂 Archivos estáticos
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "core" / "static"]

# WhiteNoise → compresión de estáticos en producción
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# 🔑 Clave primaria por defecto
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ⚙️ Configuración Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",        # Devuelve JSON por defecto
        "rest_framework.renderers.BrowsableAPIRenderer" # Habilita el navegador web de DRF (api.html)
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny"           # Público por ahora (útil en desarrollo)
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}
