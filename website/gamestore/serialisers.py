from rest_framework import serializers
from .models import Games

class gamesSerializers(serializers.ModelSerializer):
    class Meta:
        model=Games
        fields=['game_id', 'game_sku', 'game_title', 'game_genre', 'game_platform', 'game_price', 'game_quantity']


def create(self, validated_data):
     if isinstance(validated_data, list):
        return Games.objects.bulk_create([Games(**item) for item in validated_data])
     return super().create(validated_data)