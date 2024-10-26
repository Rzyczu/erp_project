from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.auth_view, name='auth'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('dashboard/teams/', include([
        path('', views.team_list_view, name='team_list'),
        path('create/', views.team_create_view, name='team_create'),
        path('join/', views.join_team_view, name='join_team_view'),  # Added for joining a team by identifier
        path('assign/', views.team_assignation_view, name='team_assignation'),
        path('<int:team_id>/', include([
            path('', views.team_page_view, name='team_page_view'),
            path('add_project/', views.add_project_view, name='add_project_view'),
            path('change_role/<int:user_id>/', views.change_role_view, name='change_role_view'),  # Added for changing role
            path('delete_user/<int:user_id>/', views.delete_user_view, name='delete_user_view'),  # Added for deleting a user from the team
            path('leave/', views.leave_team_view, name='leave_team_view'),  # Added for leaving the team
            path('projects/<int:project_id>/', include([
                path('', views.project_page_view, name='project_page_view'),
                path('add_task/', views.add_task_view, name='add_task_view'),
                path('tasks/<int:task_id>/', include([
                    path('details/', views.task_details_view, name='task_details'),
                    path('assign_to_me/', views.assign_task_to_me_view, name='assign_task_to_me'),
                    path('change_status/', views.change_task_status_view, name='change_task_status'),
                    path('edit/', views.edit_task_view, name='edit_task'),
                    path('delete/', views.delete_task_view, name='delete_task'),
                ])),
            ])),
        ])),
    ])),
]
