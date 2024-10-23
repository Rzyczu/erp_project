from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View
from .forms import UserRegisterForm, UserLoginForm

def auth_view(request):
    return render(request, 'auth.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save the form without committing to the DB
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Save the user with hashed password
            login(request, user)  # Log in the user after saving
            return redirect('dashboard')  # Redirect on successful register
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_value = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username_value, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next') or request.GET.get('next') or 'dashboard'
                return redirect(next_url)
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

class DashboardView(LoginRequiredMixin, View):
    login_url = '/login/'  # Redirect to this URL if the user is not logged in

    def get(self, request):
        users = User.objects.all()
        context = {'users': users}
        return render(request, 'erp/dashboard.html', context)

    
def logout_view(request):
    logout(request)
    return redirect('auth')
