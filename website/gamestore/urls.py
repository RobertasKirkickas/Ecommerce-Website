from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/success/', views.contact_success_view, name='contact-success'),
    path('games/', views.games, name='games'),
    path('checkout/', views.checkout, name='checkout'),  # Ensure checkout is mapped
]
