import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from django.utils.log import DEFAULT_LOGGING
from dotenv import load_dotenv

from .settings import *  # noqa: F403

load_dotenv()
DEBUG = False
BASE_DIR = Path(__file__).resolve().parent.parent
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split()
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "en-us")
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = get_random_secret_key()
    with BASE_DIR.joinpath(".env").open("a", encoding="utf-8") as file:
        file.write(f"\nSECRET_KEY={SECRET_KEY}\n")
    os.environ["SECRET_KEY"] = SECRET_KEY

default_media_root = Path.home().joinpath("packages").as_posix()
MEDIA_ROOT = os.getenv("MEDIA_ROOT", default_media_root)
DEFAULT_LOGGING["handlers"]["console"]["filters"].clear()
