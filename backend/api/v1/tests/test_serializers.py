from rest_framework import serializers
from api.v1.serializers import CadastralSerializer, LogsHistorySerializer
from api.v1.schemas import CadastralNumberSerializer


def serializer_fields_check(
        expected_fields: dict[str, serializers.Field],
        serializer: serializers.Serializer,
        ) -> None:
    """Тестирует поля указанного сериализатора."""
    assert list(serializer.fields.keys()) == list(expected_fields.keys())
    for field, field_type in expected_fields.items():
        assert isinstance(serializer.fields[field], field_type)
    return


def test_cadastral_serializer() -> None:
    """Тестирует поля сериализатора CadastralSerializer."""
    expected_fields: dict[str, any] = {
        'number': serializers.CharField,
        'latitude': serializers.FloatField,
        'longitude': serializers.FloatField,
        'status': serializers.BooleanField,
    }
    serializer_fields_check(
        expected_fields=expected_fields,
        serializer=CadastralSerializer(),
    )
    return


def test_cadastral_number_serializer() -> None:
    """Тестирует поля сериализатора CadastralNumberSerializer."""
    expected_fields: dict[str, any] = {
        'number': serializers.CharField,
    }
    serializer_fields_check(
        expected_fields=expected_fields,
        serializer=CadastralNumberSerializer(),
    )
    return


def test_log_history_serializer() -> None:
    """Тестирует поля сериализатора LogsHistorySerializer."""
    expected_fields: dict[str, any] = {
        'path': serializers.CharField,
        'method': serializers.CharField,
        'request_data': serializers.CharField,
        'status_code': serializers.IntegerField,
        'response_data': serializers.CharField,
        'cadastral': serializers.CharField,
        'datetime': serializers.DateTimeField,
    }
    serializer_fields_check(
        expected_fields=expected_fields,
        serializer=LogsHistorySerializer(),
    )
    return
