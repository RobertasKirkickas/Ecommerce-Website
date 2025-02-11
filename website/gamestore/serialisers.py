from rest_framework import serializers
from .models import Games

class gamesSerializers(serializers.ModelSerializer):
    class Meta:
        model=Games
        fields=['game_title', 'game_genre', 'game_category', 'game_platform', 'game_price', 'game_quantity', 'game_discount_price', 'image_url', 'game_description']


def create(self, validated_data):
     if isinstance(validated_data, list):
        return Games.objects.bulk_create([Games(**item) for item in validated_data])
     return super().create(validated_data)