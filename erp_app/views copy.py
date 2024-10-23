from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm

def index(request):
    return render(request, 'index.html')

def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save the form without committing to the DB
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Save the user with hashed password
            login(request, user)  # Log in the user after saving
            return redirect('home')  # Redirect on successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_value = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username_value, password=password)
            
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next') or request.GET.get('next') or 'index'
                return redirect(next_url)
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = UserLoginForm()

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
    return redirect('index')
