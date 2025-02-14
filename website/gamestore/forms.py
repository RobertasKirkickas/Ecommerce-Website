from django import forms
from django.contrib.auth.models import User
from .models import Games

# Contact
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        print(f"Sending email from {self.cleaned_data['email']} with message: {self.cleaned_data['message']}")


# AUTH
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']

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
            'game_discount_price': forms.NumberInput(attrs={'placeholder': 'e.g. 9.99', 'class':'form-control'}),
            'image_url': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'game_description': forms.Textarea(attrs={'class':'form-control'})
        }


# Checkout form
PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
)

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