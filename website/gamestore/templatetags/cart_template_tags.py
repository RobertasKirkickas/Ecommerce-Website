from django import template
from gamestore.models import Order

register = template.Library()

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)  # Corrected line
        if qs.exists():
            return qs.first().items.count()
    return 0