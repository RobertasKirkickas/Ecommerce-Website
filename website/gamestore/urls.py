from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('checkout/', views.checkout),
    path('games/', views.games),
    path('contact/', views.contact),


]
