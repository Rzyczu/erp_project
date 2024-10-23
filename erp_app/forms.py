from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password_confirm = forms.CharField(widget=forms.PasswordInput, min_length=8, label="Confirm Password")
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")
        
        return cleaned_data

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
