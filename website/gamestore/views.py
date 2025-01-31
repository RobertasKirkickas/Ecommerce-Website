from django.shortcuts import render
from .models import Games
# Create your views here.

def home(request):
    return render(request, 'index.html')

def games(request):
    allGames = Games.objects.all()
    context = {'games': allGames}
    return render(request, 'games.html', context)

def contact(request):
    return render(request, 'contact.html')

def checkout(request):
    return render(request, 'checkout.html')

