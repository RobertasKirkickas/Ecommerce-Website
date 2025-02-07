from django import forms
from django.contrib.auth.models import User
from .models import Games

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        print(f"Sending email from {self.cleaned_data['email']} with message: {self.cleaned_data['message']}")


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
        
class GamesForm(forms.ModelForm):
    class Meta:
        model = Games
        fields = '__all__'
        labels = {
            'game_id': 'Game ID',
            'game_sku': 'SKU',
            'game_title': 'Title',
            'game_genre': 'Genre',
            'game_platform': 'Platform',
            'game_price': 'Price',
            'game_quantity': 'Quantity',
        }
        widgets = {
            'game_id': forms.NumberInput(attrs={'placeholder': 'e.g. 1', 'class':'form-ctontrol'}),
            'game_sku': forms.TextInput(attrs={'placeholder': 'e.g. G0001', 'class':'form-ctontrol'}),
            'game_title': forms.TextInput(attrs={'placeholder': 'e.g. Diablo IV', 'class':'form-ctontrol'}),
            'game_genre': forms.TextInput(attrs={'placeholder': 'e.g. aRPG', 'class':'form-ctontrol'}),
            'game_platform': forms.TextInput(attrs={'placeholder': 'e.g. PC', 'class':'form-ctontrol'}),
            'game_price': forms.NumberInput(attrs={'placeholder': 'e.g. 15.99', 'class':'form-ctontrol'}),
            'game_quantity': forms.NumberInput(attrs={'placeholder': 'e.g. 5', 'class':'form-ctontrol'}),
        }