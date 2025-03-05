from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.text import slugify
from django.core.validators import RegexValidator

# Game categories
CATEGORIES_choices = [
    ('RPG', 'RPG'),
    ('Fighting', 'Fighting'),
    ('Shooter', 'Shooter'),
    ('Action', 'Action'),
    ('Racing', 'Racing'),
    ('Adventure', 'Adventure'),
    ('Sports', 'Sports')
]

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
)

# Defined model for game data
class Games(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_title = models.CharField(max_length=64)
    game_genre = models.CharField(max_length=64)
    game_category = models.CharField(choices=CATEGORIES_choices, max_length=10)
    game_platform = models.CharField(max_length=64)
    game_price = models.DecimalField(max_digits=7, decimal_places=2)  
    game_quantity = models.IntegerField()
    game_discount_price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)  
    game_description = models.TextField()
    image_url = models.ImageField(upload_to='./', default="default.png")
    slug = models.SlugField()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.game_title)  # Automatically generate slug if not provided
        super().save(*args, **kwargs)

        games_without_slug = Games.objects.filter(slug='')

        for game in games_without_slug:
            game.slug = slugify(game.game_title)  # Generates a slug from the game title
            game.save()

    def __str__(self):
        return self.game_title
    
    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'slug':self.slug})

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={'slug':self.slug})
    
    def get_remove_single_from_cart_url(self):
        return reverse('remove_single_from_cart', kwargs={'slug':self.slug})

    # Testing unit
    def get_total_price(self):
        return self.game_price * self.game_quantity

    def clean(self):
        if self.game_price<0:
            raise ValidationError('Price can not be negative')
        if self.game_quantity<0:
            raise ValidationError('Quantity can not be negative')
        

# Shopping Order
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Games, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of  {self.item.game_title}"
    
    def get_total_item_price(self):
        return self.quantity * self.item.game_price
    
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_final_price()

    def get_total_item_discount_price(self):
        return self.quantity * self.item.game_discount_price
    
    def get_final_price(self):
        if self.item.game_discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()

# Customer's order
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

# Customer details collection on checkout    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    street_address = models.CharField(max_length=200)
    apartment_address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=20)
    post_code = models.CharField(max_length=10)
    save_info = models.BooleanField(default=False)
    default = models.BooleanField(default=False)
    use_default = models.BooleanField(default=False)
    payment_option = models.CharField(choices=PAYMENT_CHOICES, max_length=2)

    def __str__(self):
        return self.user.username

    # Ensure only one default address per user
    def save(self, *args, **kwargs):
        if self.default:
            Address.objects.filter(user=self.user, default=True).exclude(id=self.id).update(default=False)
        super().save(*args, **kwargs)
