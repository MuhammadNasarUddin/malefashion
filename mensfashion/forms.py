from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')

# your_app_name/forms.py



class EmailAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        email = self.cleaned_data.get('username')
        if email:
            return email.lower()  # Normalize the email address
