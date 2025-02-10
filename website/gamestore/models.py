from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Games(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_sku = models.CharField(max_length=50, unique=True)
    game_title = models.CharField(max_length=64)
    game_genre = models.CharField(max_length=64)
    game_platform = models.CharField(max_length=64)
    game_price = models.DecimalField(max_digits=7, decimal_places=2)  
    game_quantity = models.IntegerField()
    image_url = models.CharField(max_length=255, default="images/game-images/default.jpg")

    def __str__(self):
        return self.game_title
    
    def get_total_price(self):
        return self.game_price * self.game_quantity

    def clean(self):
        if self.game_price<0:
            raise ValidationError('Price can not be negative')
        if self.game_quantity<0:
            raise ValidationError('Stock can not be negative')