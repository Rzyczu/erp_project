from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth_view, name='auth'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('teams/', views.team_list_view, name='team_list'),
    path('teams/create/', views.team_create_view, name='team_create'),
    path('teams/assign/', views.team_assignation_view, name='team_assignation'),
    
    path('teams/<int:team_id>/', views.team_page_view, name='team_page_view'),
    path('teams/<int:team_id>/add_project/', views.add_project_view, name='add_project_view'),
    path('projects/<int:project_id>/', views.project_page_view, name='project_page_view'),
    path('projects/<int:project_id>/add_task/', views.add_task_view, name='add_task_view'),
    
    path('tasks/<int:task_id>/details/', views.task_details_view, name='task_details'),
    path('tasks/<int:task_id>/assign_to_me/', views.assign_task_to_me_view, name='assign_task_to_me'),
    path('tasks/<int:task_id>/change_status/', views.change_task_status_view, name='change_task_status'),
    path('tasks/<int:task_id>/edit/', views.edit_task_view, name='edit_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task_view, name='delete_task'),
]
