from django.db import models

# Create your models here.

class Games(models.Model):
    game_title = models.CharField(max_length=64)
    game_genre = models.CharField(max_length=64)
    game_platform = models.CharField(max_length=64)
    game_price = models.DecimalField(max_digits=5, decimal_places=2)


    def __str__(self):
        return (f"ID:{self.id} Game: {self.game_title} "
                f"Genre: {self.game_genre} Platform: {self.game_platform} Price: £{self.game_price}")
