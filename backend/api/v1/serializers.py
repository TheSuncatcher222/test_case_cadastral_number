from rest_framework import serializers

from cadastral.models import CadastralNumber


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
