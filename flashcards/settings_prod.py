from .settings_base import *

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")
