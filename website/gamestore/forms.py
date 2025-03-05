from django import forms
from django.contrib.auth.models import User
from .models import Games
import re
# Contact
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        print(f"Sending email from {self.cleaned_data['email']} with message: {self.cleaned_data['message']}")


# AUTH
class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        help_text=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Check minimum length
        if len(username) < 4:
            raise forms.ValidationError("Username must be at least 4 characters long.")

        # Check for special symbols
        if not re.match(r'^[a-zA-Z0-9]+$', username):  # Allows only letters, numbers, and underscore
            raise forms.ValidationError("Username can only contain letters and numbers.")

        return username
    
    # Ensures user uses strong password
    def clean_password(self):
        password = self.cleaned_data.get('password')

        # 
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long, including 1 uppercase letter, 1 special character, and 1 digit.")
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least 1 uppercase letter.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least 1 digit.")
        if not any(char in "!@#$%^&*()-_=+[{]};:'\",<.>/?`~" for char in password):
            raise forms.ValidationError("Password must contain at least 1 special character.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        # Check if passwords match
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data


# Form for editing / adding games to the system.
class GamesForm(forms.ModelForm):
    class Meta:
        model = Games
        fields = ['game_title', 'game_genre', 'game_category', 'game_platform', 'game_price', 'game_quantity', 'game_discount_price', 'image_url', 'game_description']

        labels = {
            'game_title': 'Title',
            'game_genre': 'Genre',
            'game_category': 'Category',
            'game_platform': 'Platform',
            'game_price': 'Price',
            'game_quantity': 'Quantity',
            'game_discount_price': 'Discount Price',
            'image_url': "Image",
            'game_description': 'Description'
        }
        
        widgets = {
            'game_title': forms.TextInput(attrs={'placeholder': 'e.g. Diablo IV', 'class':'form-control'}),
            'game_genre': forms.TextInput(attrs={'placeholder': 'e.g. aRPG', 'class':'form-control'}),
            'game_category': forms.Select(attrs={'class':'form-control'}),
            'game_platform': forms.TextInput(attrs={'placeholder': 'e.g. PC', 'class':'form-control'}),
            'game_price': forms.NumberInput(attrs={'placeholder': 'e.g. 15.99', 'class':'form-control'}),
            'game_quantity': forms.NumberInput(attrs={'placeholder': 'e.g. 5', 'class':'form-control'}),
            'game_discount_price': forms.NumberInput(attrs={'placeholder': 'e.g. 9.99', 'class': 'form-control'}),
            'image_url': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'game_description': forms.Textarea(attrs={'class':'form-control'})
        }


# Checkout form
PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
)

# Form for customer to fill at the checkout
class AddressForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    street_address = forms.CharField()
    apartment_address = forms.CharField(required=False)
    city = forms.CharField()
    post_code = forms.CharField(required=False)
    save_info = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)  