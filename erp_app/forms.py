from django import forms
from django.core.exceptions import ValidationError
from .models import User
    
class ContactForm(forms.Form):
    name = forms.CharField(required=False, max_length=64)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
    
    def send_email(self):
        print (f"Sending email from: {self.cleaned_data['email']}")
        
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password_confirm = forms.CharField(widget=forms.PasswordInput, min_length=8, label="Confirm Password")
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['name', 'surname', 'login', 'password', 'email']
        
    def clean_mail(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_login(self):
        login = self.cleaned_data.get('login')
        if User.objects.filter(login=login).exists():
            raise ValidationError("This login is already taken.")
        return login
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password!=password_confirm:
            raise ValidationError("Passwords do not match.")
        return self.cleaned_data
    
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)