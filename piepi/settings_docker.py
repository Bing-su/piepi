import logging
import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from django.utils.log import DEFAULT_LOGGING
from dotenv import find_dotenv, load_dotenv, set_key

from .settings import *  # noqa: F403

logger = logging.getLogger("piepi")
dotenv_path = Path(find_dotenv() or Path(__file__).parent.parent.joinpath(".env"))
dotenv_path.touch(exist_ok=True)
load_dotenv(dotenv_path)

DEBUG = False
BASE_DIR = Path(__file__).resolve().parent.parent

LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "en-us")
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = get_random_secret_key()
    set_key(dotenv_path, "SECRET_KEY", SECRET_KEY)

default_media_root = BASE_DIR.joinpath("packages").as_posix()
MEDIA_ROOT = os.getenv("MEDIA_ROOT", default_media_root)
DEFAULT_LOGGING["handlers"]["console"]["filters"].clear()

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split()
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split()
CORS_URLS_REGEX = os.getenv("CORS_URLS_REGEX", r"^.*$")
CORS_ORIGIN_ALLOW_ALL = os.getenv("CORS_ORIGIN_ALLOW_ALL", "false").lower() == "true"
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split()
