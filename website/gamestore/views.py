from django.shortcuts import render, redirect, get_object_or_404
from .models import Games, Order, OrderItem, Address
from .forms import ContactForm, AddressForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
# For class-based views[CBV]
from django.contrib.auth.mixins import LoginRequiredMixin
# For class-based views[CBV]
from django.views import View
# Import the User class (model)
from django.contrib.auth.models import User
# Import the RegisterForm from forms.py
from .forms import RegisterForm
from .forms import GamesForm
from .serialisers import gamesSerializers
from django.views.decorators.http import require_http_methods
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist



class GameDetail(DetailView):
    model = Games
    template_name = 'game.html'
    context_object_name = 'game'

class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order':order
        }
        return render(self.request, 'order_summary.html', context)


# Normal pages
def home(request):
    all_games = Games.objects.all()
    return render(request, 'index.html', {'games': all_games})

def profile(request):
    return render(request, 'accounts/profile.html')

def profile_confirm_delete(request):
    return render(request, 'accounts/profile_confirm_delete.html')

@login_required
def delete_profile(request, username):
    if request.method == "POST":
        if request.user.username == username:  # Ensure user can only delete their own profile
            try:
                request.user.delete()
                messages.success(request, "Your account has been deleted!")
                return redirect('home')  # Redirect to homepage
            except Exception as e:
                messages.error(request, "An error occurred while deleting your account.")
                return redirect('profile')  # Redirect back to profile page
        else:
            messages.error(request, "You can only delete your own profile.")
            return redirect('profile')
    
    return render(request, 'accounts/profile.html')


class SearchView(ListView):
    model = Games
    template_name = 'components/search.html'
    context_object_name = 'search_games'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = Games.objects.filter(game_title__contains=query)
            result = postresult
        else:
            result = None
        return result

# Checkout
class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            order = None  # Prevent errors if no active order exists

        context = {
            'order': order
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            messages.error(self.request, "No active order found.")
            return redirect('checkout')

        # Get form data from POST request
        first_name = self.request.POST.get('first_name')
        last_name = self.request.POST.get('last_name')
        email = self.request.POST.get('email')
        street_address = self.request.POST.get('street_address')
        apartment_address = self.request.POST.get('apartment_address', '')
        city = self.request.POST.get('city')
        post_code = self.request.POST.get('post_code')
        payment_option = self.request.POST.get('payment_option')

        # Validate required fields
        if not all([first_name, last_name, email, street_address, city, post_code, payment_option]):
            messages.error(self.request, "Please fill in all required fields.")
            return redirect('checkout')

        # Save info
        address = Address.objects.create(
            user=self.request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            street_address=street_address,
            apartment_address=apartment_address,
            city=city,
            post_code=post_code
        )

        # Save payment option and link info to order
        order.address = address
        order.payment_option = payment_option
        order.ordered = True
        order.save()

        # Remove all items from the order
        order.items.all().delete()  # Make the cart empty
        messages.success(self.request, "Order Submitted!")
        return redirect('checkout')

        

# CART
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Games, slug=slug)

    # Ensure user is authenticated before proceeding
    if request.user.is_authenticated:
        order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]

            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                messages.success(request, f"{item.game_title}'s quantity was updated!")
            else:
                order.items.add(order_item)
                order.save()
                messages.success(request, f"{item.game_title} was added to your cart!")

        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, ordered=False, ordered_date=ordered_date)
            order.items.add(order_item)
            order.save()

        return redirect('order_summary')

    else:
        messages.warning(request, "You need to log in to add items to your cart.")
        return redirect('login')  # Redirect to login page if user is not authenticated
    
def remove_from_cart(request, slug):
    item = get_object_or_404(Games, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order.items.remove(order_item)
            order.save()
            messages.success(request, f"{item.game_title} was removed from your cart!")
            return redirect('order_summary')
        else:
            messages.info(request, f"{item.game_title} was not in your cart!")
            return redirect('order_summary')
    else:
        messages.info(request, "You don't have an active order!")
        return redirect('order_summary')

def remove_single_from_cart(request, slug):
    item = get_object_or_404(Games, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order.save()

            messages.success(request, f"{item.game_title}'s quantity was updated!")
            return redirect('order_summary')
        else:
            messages.info(request, f"{item.game_title} was not in your cart!")
            return redirect('order_summary')
    else:
        messages.info(request, "You don't have an active order!")
        return redirect('order_summary')

# CONTACT
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


def game_detail(request, pk):
    game = get_object_or_404(Games, pk=pk)
    return render(request, 'game.html', {'game': game})



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


# Function to check if user is admin or moderator
def is_admin_or_mod(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# Index view
@login_required(login_url='/login/')
@user_passes_test(is_admin_or_mod)
def game_index_view(request):
    return render(request, 'crud/index.html')

# Create View
@login_required(login_url='/login/')
@user_passes_test(is_admin_or_mod)
def game_create_view(request):
    form = GamesForm()
    if request.method == 'POST':
        form = GamesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('game_list')
    return render(request, 'crud/game_form.html', {'form': form})

# Read View
@login_required(login_url='/login/')
@user_passes_test(is_admin_or_mod)
def game_list_view(request):
    games = Games.objects.all()
    return render(request, 'crud/game_list.html', {'games': games})

# Update View
@login_required(login_url='/login/')
@user_passes_test(is_admin_or_mod)
def game_update_view(request, game_id):
    # Get the specific game object using the primary key (game_id)
    game = get_object_or_404(Games, pk=game_id)
    form = GamesForm(instance=game)
    if request.method == "POST":
        form = GamesForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect('game_list')
    return render(request, 'crud/game_form.html', {'form': form})

# Delete View
@login_required(login_url='/login/')
@user_passes_test(is_admin_or_mod)
def game_delete_view(request, game_id):
    game = Games.objects.get(game_id=game_id)
    if request.method == "POST":
        game.delete()
        return redirect('game_list')
    return render(request, 'crud/game_confirm_delete.html', {'game': game})


# API for Listing and Creating Games (Admin only)
class gamesListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]  # Only admin users can access
    queryset = Games.objects.all()
    serializer_class = gamesSerializers

    def create(self, request, *args, **kwargs):
        # Check if the request contains multiple objects
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# API for Retrieving, Updating, and Deleting a Game (Admin only)
class gamesRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]  # Only admin users can access
    queryset = Games.objects.all()
    serializer_class = gamesSerializers
    lookup_field = 'pk'  # Deleting using the primary key