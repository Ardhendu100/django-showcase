# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import random


class SignUpForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, max_length=15)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered")
        return email
    
    def generate_username(self, first_name):
        # Create a base username
        base_username = f"{first_name.lower().replace(' ', '').strip()}"
        
        random_digit = random.randint(1000, 9999)
        
        # Combine base username with random digit
        username = f"{base_username}{random_digit}"
        
        # Ensure uniqueness of username
        while User.objects.filter(username=username).exists():
            random_digit = random.randint(0, 9)  # Generate a new random digit
            username = f"{base_username}{random_digit}"
        
        return username
