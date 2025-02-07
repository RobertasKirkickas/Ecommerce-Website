from django.shortcuts import render, redirect
from .models import Games
from .forms import ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# For class-based views[CBV]
from django.contrib.auth.mixins import LoginRequiredMixin
# For class-based views[CBV]
from django.views import View
# Import the User class (model)
from django.contrib.auth.models import User
# Import the RegisterForm from forms.py
from .forms import RegisterForm
from .forms import GamesForm
# from .serialisers import gamesSerializers

# Normal pages
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


# Authentication
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()  

    return render(request, 'accounts/register.html', {'form': form}) 




def login_view(request):
    error_message = None  # Initialize the variable

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            error_message = "Wrong username and/or password!"

    return render(request, 'accounts/login.html', {'error': error_message})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    else:
        return redirect('home')



# Home View
# Using decorator

@login_required
def home_view(request):
    return render(request, 'index.html')

# Protected View - Inventory Management System and etc.
class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'
    # 'next' - to redirect URL
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'crud/index.html')
    


# CRUD

# Index view
@login_required(login_url='/login/')
def game_index_view(request):
    return render(request, 'crud/index.html')

# Create View
@login_required(login_url='/login/')
def game_create_view(request):
    form = GamesForm()
    if request.method == 'POST':
        form = GamesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('game_list')
    return render(request, 'crud/game_form.html', {'form':form})


# Read View
@login_required(login_url='/login/')
def game_list_view(request):
    games = Games.objects.all()
    return render(request, 'crud/game_list.html', {'games':games})



# Update View
@login_required(login_url='/login/')
def game_update_view(request, game_id):
    game = Games.objects.get(game_id=game_id)
    form = GamesForm(instance=game)
    if request.method == "POST":
        form = GamesForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('game_list')
    return render(request, 'crud/game_form.html', {'form':form})



# Delete View
@login_required(login_url='/login/')
def game_delete_view(request, game_id):
    game = Games.objects.get(game_id=game_id)
    if request.method == "POST":
        game.delete()
        return redirect('game_list')
    return render(request, 'crud/game_confirm_delete.html', {'game': game})