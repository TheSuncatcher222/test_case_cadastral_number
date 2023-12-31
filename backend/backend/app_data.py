import os
from pathlib import Path

from dotenv import load_dotenv


"""App data."""


BASE_DIR: Path = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'), verbose=True)


"""Django data."""


DB_ENGINE: str = os.getenv('DB_ENGINE')
DB_USER: str = os.getenv('POSTGRES_USER')
DB_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
DB_HOST: str = os.getenv('DB_HOST')
DB_PORT: str = os.getenv('DB_PORT')
DB_NAME: str = os.getenv('POSTGRES_DB')

DATABASE_POSTGRESQL: dict[str, dict[str, str]] = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

DATABASE_SQLITE: dict[str, dict[str, str]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

HTTP_METHOD_NAME_MAX_LEN: int = 10

RESPONSE_DATA_API_AVAILABLE: dict[str, str] = {'message': 'API функционирует.'}

URL_PATH_MAX_LEN: int = 255

"""Models data."""


ADMIN_LIST_PER_PAGE: int = 15

CADASTRAL_NUMBER_LEN: int = 16

CADASTRAL_NUMBER_ANY: int = 255


"""Security data."""


SECRET_KEY: str = os.getenv('SECRET_KEY')


"""URL data."""


EXTERNAL_SERVER_URL: str = (
    'http://cadastral_external_server:8000/validate_cadastral/'
)

PATH_API_V1: str = '/api/v1/'
PATH_QUERY: str = f'{PATH_API_V1}query/'
PATH_RESULT: str = f'{PATH_API_V1}result/'
