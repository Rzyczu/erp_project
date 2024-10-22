from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserRegistrationForm, UserLoginForm
from .models import User
from django.http import HttpResponse


# Create your views here.
# def index(request):
#     #return HttpResponse("Hello, World! This is the Warehouse application.")
#     users = User.objects.all()
#     contex = {'users': users}
#     return render(request, 'index.html', contex)

def index(request):
    return render(request, 'index.html')

def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user and get the user instance
            login(request, user)  # Log in the user after saving
            return redirect('home')  # Redirect on successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Logowanie użytkownika
                next_url = request.POST.get('home') or request.GET.get('home') or 'index'
                return redirect('next_url')  # Przekierowanie po zalogowaniu
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def home_view(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'home.html', context)
