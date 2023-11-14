from rest_framework import serializers

from cadastral.models import CadastralNumber, LogsHistory


class CadastralSerializer(serializers.ModelSerializer):
    """Сериализатор модели CadastralNumber."""

    class Meta:
        model = CadastralNumber
        fields = (
            'number',
            'latitude',
            'longitude',
            'status',
        )
        read_only_fields = (
            'status',
        )


class LogsHistorySerializer(serializers.ModelSerializer):
    """Сериализатор модели LogsHistory."""

    class Meta:
        model = LogsHistory
        fields = (
            'path',
            'method',
            'request_data',
            'status_code',
            'response_data',
            'cadastral',
            'datetime',
        )
        read_only_fields = fields
