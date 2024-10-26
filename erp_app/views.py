from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.http import JsonResponse, HttpResponseRedirect
import json
from django.utils.dateformat import format

from .forms import UserRegisterForm, UserLoginForm, TeamForm, TeamUserForm, TeamUserRoleForm, ProjectForm, TaskForm
from .models import Team, TeamUserRole, Project, Task
from .decorators import project_manager_required

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
    login_url = '/login/'

    def get(self, request):
        user = request.user
        # Retrieve teams using the `TeamUserRole` relationship
        user_teams = Team.objects.filter(teamuserrole__user=user).distinct()
        
        context = {
            'user_teams': user_teams,
        }
        return render(request, 'erp/dashboard.html', context)

# @login_required
# def dashboard_view(request):
#     user = request.user
#     teams = user.teams.all()
#     context = {'teams': teams}
#     return render(request, 'erp/dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('auth')

@login_required
def team_list_view(request):
    teams = Team.objects.prefetch_related('teamuserrole_set__user').all()  # Prefetch roles
    return render(request, 'teams/list.html', {'teams': teams})

@login_required
def team_create_view(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form = TeamForm()
    return render(request, 'teams/form.html', {'form': form})

@login_required
def assign_users_to_team_view(request): 
    if request.method == 'POST':
        form = TeamUserForm(request.POST)
        if form.is_valid():
            team = form.cleaned_data['team']
            users = form.cleaned_data['users']
            team.users.set(users)
            return redirect('team_list')
    else:
        form = TeamUserForm()
    return render(request, 'teams/assignation.html', {'form': form}) 

@login_required
def team_assignation_view(request):
    if request.method == 'POST':
        form = TeamUserRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            if role == 'project_manager' and not request.user.is_superuser:
                form.add_error('role', "Only superusers can assign the Project Manager role.")
            else:
                form.save()
                return redirect('team_list')
    else:
        form = TeamUserRoleForm()
    return render(request, 'teams/assignation.html', {'form': form})

@login_required
def team_page_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    projects = team.projects.all()
    team_members = TeamUserRole.objects.filter(team=team)
    context = {
        'team': team,
        'projects': projects,
        'team_members': team_members,
    }
    return render(request, 'teams/team_page.html', context)

@login_required
def project_page_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.order_by('status')
    team_members = TeamUserRole.objects.filter(team=project.team)
    
    # Grupowanie zadań według użytkowników i statusów
    tasks_by_user = {}
    for member in team_members:
        user_tasks = tasks.filter(assigned_user=member.user)
        if user_tasks.exists():
            tasks_by_user[member] = {
                'user_tasks': {
                    status: user_tasks.filter(status=status)
                    for status, _ in Task.STATUS_CHOICES if user_tasks.filter(status=status).exists()
                }
            }

    # Filtracja zadań bez przypisanego użytkownika
    unassigned_tasks = tasks.filter(assigned_user__isnull=True)

    context = {
        'project': project,
        'tasks_by_user': tasks_by_user,
        'team_members': team_members,
        'unassigned_tasks': unassigned_tasks,  # Przekazujemy przefiltrowane zadania do szablonu
    }
    return render(request, 'projects/project_page.html', context)

@login_required
@project_manager_required
def add_project_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.team = team
            project.save()
            return redirect('team_page_view', team_id=team.id)
    else:
        form = ProjectForm()
    return render(request, 'projects/add_project.html', {'form': form, 'team': team})

@login_required
def add_task_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, project=project)  # Pass project to form
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            # Load milestones as JSON list from request and assign to task
            milestones = json.loads(request.POST.get('milestones', '[]'))
            task.milestones = milestones
            task.save()
            return redirect('project_page_view', project_id=project.id)
    else:
        form = TaskForm(project=project)

    return render(request, 'projects/add_task.html', {'form': form, 'project': project})



@login_required
def task_details_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    data = {
        'name': task.name,
        'description': task.description,
        'due_date': task.due_date,
        'assigned_user': task.assigned_user.get_full_name() if task.assigned_user else 'Unassigned',
        'status': task.get_status_display(),
        'milestones': task.milestones if isinstance(task.milestones, list) else [],  # Directly use the list if available
        'images': [task.images.url] if task.images else [],  # Handle single image field as a list
    }
    return JsonResponse(data)

@require_POST
@login_required
def assign_task_to_me_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.assigned_user = request.user
    task.save()
    return JsonResponse({'status': 'assigned'})

@require_POST
@login_required
def change_task_status_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
    except (ValueError, KeyError):
        return JsonResponse({'error': 'Invalid data'}, status=400)

    if new_status in dict(Task.STATUS_CHOICES):
        task.status = new_status
        task.save()
        return JsonResponse({'status': 'changed'})
    return JsonResponse({'error': 'Invalid status'}, status=400)

import json
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

@login_required
def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project = task.project

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task, project=project)
        if form.is_valid():
            milestones = request.POST.get('milestones', '[]')
            task.milestones = json.loads(milestones) if milestones else []  # Parse as JSON array
            form.save()
            return redirect('project_page_view', project_id=project.id)
    else:
        milestones = json.loads(task.milestones) if isinstance(task.milestones, str) else task.milestones or []
        form = TaskForm(instance=task, project=project)

    return render(request, 'projects/edit_task.html', {
        'form': form,
        'project': project,
        'task': task,
        'milestones': milestones  # Pass milestones directly to the context
    })



@require_POST
@login_required
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return JsonResponse({'status': 'deleted'})