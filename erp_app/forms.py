from django import forms
from django.core.exceptions import ValidationError
from .models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password_confirm = forms.CharField(widget=forms.PasswordInput, min_length=8, label="Confirm Password")
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['name', 'surname', 'login', 'password', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_login(self):
        login = self.cleaned_data.get('login')
        if User.objects.filter(login=login).exists():
            raise ValidationError("This login is already taken.")
        return login
    
    # Use clean method to compare passwords
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")
        
        return cleaned_data  # Return the whole cleaned_data after validation

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)