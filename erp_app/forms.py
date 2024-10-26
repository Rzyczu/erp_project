from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Team, TeamUserRole, Project, Task

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

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']

class TeamUserForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all())
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)
    
class TeamUserRoleForm(forms.ModelForm):
    class Meta:
        model = TeamUserRole
        fields = ['team', 'user', 'role']
        widgets = {
            'role': forms.Select(choices=TeamUserRole.ROLE_CHOICES),
        }
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)  # Pobieramy obiekt projektu
        super().__init__(*args, **kwargs)
        
        # Filtrujemy użytkowników dostępnych do przypisania na członków zespołu projektu
        if project:
            team_users = TeamUserRole.objects.filter(team=project.team).values_list('user', flat=True)
            self.fields['assigned_user'].queryset = User.objects.filter(id__in=team_users)

    class Meta:
        model = Task
        fields = ['name', 'description', 'assigned_user', 'due_date', 'status', 'images']