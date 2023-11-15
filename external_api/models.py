import re

import pydantic

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


class CadastralNumber(pydantic.BaseModel):
    """Класс представления кадастрового номера."""

    number: str
    latitude: float
    longitude: float

    @staticmethod
    def _validate(string: str, pattern: str, err: str) -> None:
        """
        Производит валидацию строки по указанному паттерну.
        Вызывает ValueError, если значение не соответствует.
        Возвращает None.
        """
        if not re.fullmatch(pattern=pattern, string=string):
            raise ValueError(err)
        return

    @pydantic.validator('number')
    def validate_number(cls, value: str) -> str:
        """Производит валидацию кадастрового номера."""
        cls._validate(
            string=value,
            pattern=CADASTRAL_NUMBER_PATTERN,
            err=CADASTRAL_NUMBER_ERR,
        )
        return value

    @pydantic.validator('latitude')
    def validate_latitude(cls, value: float) -> float:
        """
        Производит валидацию координаты широты в десятичном представлении.
        """
        cls._validate(
            string=str(value),
            pattern=CADASTRAL_LAT_LON_PATTERN,
            err=CADASTRAL_LAT_ERR,
        )
        return value

    @pydantic.validator('longitude')
    def validate_longitude(cls, value: float) -> float:
        """
        Производит валидацию координаты долготы в десятичном представлении.
        """
        cls._validate(
            string=str(value),
            pattern=CADASTRAL_LAT_LON_PATTERN,
            err=CADASTRAL_LON_ERR,
        )
        return value
