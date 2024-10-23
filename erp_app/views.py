from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .forms import UserRegistrationForm, UserLoginForm
from .models import User

def index(request):
    return render(request, 'index.html')

def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save the form without committing to the DB
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Now save the user with hashed password
            login(request, user)  # Log in the user after saving
            return redirect('home')  # Redirect on successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            login_value = form.cleaned_data['username']  # Pobieramy login użytkownika
            password = form.cleaned_data['password']
            
            # Używamy loginu zamiast username
            user = authenticate(request, username=login_value, password=password)
            
            if user is not None:
                login(request, user)  # Logowanie użytkownika
                next_url = request.POST.get('next') or request.GET.get('next') or 'index'
                return redirect(next_url)  # Przekierowanie po zalogowaniu
            else:
                form.add_error(None, "Invalid username or password.")  # Błąd logowania
    else:
        form = UserLoginForm()  # Inicjalizacja formularza dla metody GET

    return render(request, 'login.html', {'form': form})



def home_view(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'home.html', context)

class ProtectedView(LoginRequiredMixin, View): 
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    
    def get(self, request):
        return render(request, 'protected.html')
    
def logout_view(request):
    logout(request)
    return redirect('index')  # Przekierowanie po wylogowaniu
