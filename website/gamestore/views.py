from django.shortcuts import render, redirect
from .models import Games
from .forms import ContactForm  # Ensure this is in forms.py

def home(request):
    allGames = Games.objects.all()
    return render(request, 'index.html', {'games': allGames})

def games(request):
    allGames = Games.objects.all()
    return render(request, 'games.html', {'games': allGames})

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_email()  # Placeholder for actual email sending
            return redirect('contact-success')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def contact_success_view(request):
    return render(request, 'forms/contact_success.html')

def checkout(request):
    return render(request, 'checkout.html')
