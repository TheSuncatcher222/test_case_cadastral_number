import re

from django.core.exceptions import ValidationError

CADASTRAL_NUMBER_PATTERN: str = r'^\d{2}:\d{2}:\d{6}:\d{3}$'
CADASTRAL_NUMBER_ERR: str = (
    'Укажите корректный кадастровый номер вида XX:XX:XXXXXX:XX.'
)
CADASTRAL_LAT_LON_PATTERN: str = r'^\d{2}.\d{0,6}'
CADASTRAL_LAT_ERR: str = (
    'Укажите корректные координаты широты вида XX.XXXXXX.'
)
CADASTRAL_LON_ERR: str = (
    'Укажите корректные координаты долготы вида XX.XXXXXX.'
)


def validate_string(value: str, pattern: str, err: str) -> None:
    """
    Производит валидацию строки по указанному паттерну.
    Вызывает ValueError, если значение не соответствует.
    Возвращает None.
    """
    if not re.fullmatch(pattern=pattern, string=value):
        raise ValidationError(err)
    return


def validate_cadastral_number(value: str) -> str:
    """Производит валидацию кадастрового номера."""
    validate_string(
        value=str(value),
        pattern=CADASTRAL_NUMBER_PATTERN,
        err=CADASTRAL_NUMBER_ERR,
    )
    return value


def validate_cadastral_lat(value: float) -> float:
    """Производит валидацию координаты широты в десятичном представлении."""
    validate_string(
        value=str(value),
        pattern=CADASTRAL_LAT_LON_PATTERN,
        err=CADASTRAL_LAT_ERR,
    )
    return value


def validate_cadastral_lon(value: float) -> float:
    """Производит валидацию координаты долготы в десятичном представлении."""
    validate_string(
        value=str(value),
        pattern=CADASTRAL_LAT_LON_PATTERN,
        err=CADASTRAL_LON_ERR,
    )
    return value
