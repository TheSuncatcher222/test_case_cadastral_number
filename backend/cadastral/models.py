from django.db import models

from backend.app_data import CADASTRAL_NUMBER_LEN
from cadastral.validators import (
    validate_cadastral_number,
    validate_cadastral_lat,
    validate_cadastral_lon,
)


class CadastralNumber(models.Model):
    """Класс представления кадастрового номера."""

    number = models.CharField(
        verbose_name='Кадастровый номер',
        max_length=CADASTRAL_NUMBER_LEN,
        unique=True,
        validators=(validate_cadastral_number,),
    )
    latitude = models.FloatField(
        verbose_name='Широта (десятичные градусы)',
        validators=(validate_cadastral_lat,),
    )
    longitude = models.FloatField(
        verbose_name='Долгота (десятичные градусы)',
        validators=(validate_cadastral_lon,),
    )
    status = models.BooleanField(
        verbose_name='Статус',
        default=None,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Кадастровый номер'
        verbose_name_plural = 'Кадастровые номера'

    def str(self):
        return self.number
