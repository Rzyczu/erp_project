from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from django.db import transaction
from .forms import UserRegisterForm, UserLoginForm, TeamForm, TeamUserForm, TeamUserRoleForm, ProjectForm, TaskForm
from .models import Team, TeamUserRole, Project, Task
from .decorators import project_manager_required
import json

def auth_view(request):
    return render(request, 'auth.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
            return redirect(request.POST.get('next') or 'dashboard')
        form.add_error(None, "Invalid username or password.")
    return render(request, 'accounts/login.html', {'form': form})

class DashboardView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        user = request.user
        user_teams = Team.objects.filter(teamuserrole__user=user).distinct()
        return render(request, 'erp/dashboard.html', {'user_teams': user_teams})

def logout_view(request):
    logout(request)
    return redirect('auth')

@login_required
def team_list_view(request):
    teams = Team.objects.prefetch_related('teamuserrole_set__user')
    return render(request, 'erp/teams/list.html', {'teams': teams})

@login_required
def team_create_view(request):
    form = TeamForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('team_list')
    return render(request, 'erp/teams/form.html', {'form': form})

@login_required
def team_assignation_view(request):
    form = TeamUserRoleForm(request.POST or None)
    if form.is_valid():
        role = form.cleaned_data['role']
        if role == 'project_manager' and not request.user.is_superuser:
            form.add_error('role', "Only superusers can assign the Project Manager role.")
        else:
            form.save()
            return redirect('team_list')
    return render(request, 'erp/teams/assignation.html', {'form': form})

@login_required
def team_page_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    projects = team.projects.select_related('team')
    team_members = TeamUserRole.objects.filter(team=team)
    return render(request, 'erp/teams/team_page.html', {
        'team': team,
        'projects': projects,
        'team_members': team_members,
    })

@login_required
def project_page_view(request, team_id, project_id):
    project = get_object_or_404(Project, id=project_id, team_id=team_id)
    tasks = project.tasks.select_related('assigned_user').order_by('status')
    team_members = TeamUserRole.objects.filter(team=project.team)

    tasks_by_user = {
        member: {
            'user_tasks': {
                status: tasks.filter(status=status, assigned_user=member.user)
                for status, _ in Task.STATUS_CHOICES
            }
        }
        for member in team_members if tasks.filter(assigned_user=member.user).exists()
    }

    unassigned_tasks = tasks.filter(assigned_user__isnull=True)

    return render(request, 'erp/projects/project_page.html', {
        'project': project,
        'tasks_by_user': tasks_by_user,
        'team_members': team_members,
        'unassigned_tasks': unassigned_tasks,
    })


@login_required
@project_manager_required
def add_project_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.team = team
        project.save()
        return redirect('team_page_view', team_id=team.id)
    return render(request, 'erp/projects/add_project.html', {'form': form, 'team': team})

@login_required
def task_details_view(request, team_id, project_id, task_id):
    task = get_object_or_404(Task, id=task_id, project__id=project_id, project__team__id=team_id)
    data = {
        'name': task.name,
        'description': task.description,
        'due_date': task.due_date,
        'assigned_user': task.assigned_user.get_full_name() if task.assigned_user else 'Unassigned',
        'status': task.get_status_display(),
        'milestones': task.milestones if isinstance(task.milestones, list) else [],
        'images': [task.images.url] if task.images else [],
    }
    return JsonResponse(data)

@login_required
def add_task_view(request, team_id, project_id):
    project = get_object_or_404(Project, id=project_id, team__id=team_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            milestones = json.loads(request.POST.get('milestones', '[]'))
            task.milestones = milestones
            task.save()
            return redirect('project_page_view', team_id=team_id, project_id=project.id)
    else:
        form = TaskForm(project=project)
    
    return render(request, 'erp/tasks/add_task.html', {'form': form, 'project': project})

@login_required
def edit_task_view(request, team_id, project_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    form = TaskForm(request.POST or None, request.FILES or None, instance=task, project=task.project)
    if form.is_valid():
        # Parse the milestones field if provided
        milestones = request.POST.get('milestones', '[]')
        try:
            task.milestones = json.loads(milestones) if isinstance(milestones, str) else milestones
        except json.JSONDecodeError:
            task.milestones = []
        form.save()
        return redirect('project_page_view', team_id=team_id, project_id=project_id)
    
    # Directly use the milestones if they are already a list
    milestones = task.milestones if isinstance(task.milestones, list) else json.loads(task.milestones or '[]')
    
    return render(request, 'erp/tasks/edit_task.html', {
        'form': form,
        'project': task.project,
        'task': task,
        'milestones': milestones
    })

@require_POST
@login_required
def assign_task_to_me_view(request, team_id, project_id, task_id):
    # Get the task object ensuring it matches the provided team and project
    task = get_object_or_404(Task, id=task_id, project__id=project_id, project__team__id=team_id)
    task.assigned_user = request.user
    task.save()
    return JsonResponse({'status': 'assigned'})

@require_POST
@login_required
def change_task_status_view(request, team_id, project_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            return JsonResponse({'status': 'changed'})
        return JsonResponse({'error': 'Invalid status'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid data'}, status=400)

@require_POST
@login_required
def delete_task_view(request, team_id, project_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return JsonResponse({'status': 'deleted'})
