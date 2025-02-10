from rest_framework import serializers
from .models import Games

class gamesSerializers(serializers.ModelSerializer):
    class Meta:
        model=Games
        fields=['game_id', 'game_sku', 'game_title', 'game_genre', 'game_platform', 'game_price', 'game_quantity']

