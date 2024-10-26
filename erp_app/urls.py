# urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.auth_view, name='auth'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/teams/', include([
        path('', views.team_list_view, name='team_list'),
        path('create/', views.team_create_view, name='team_create'),
        path('assign/', views.team_assignation_view, name='team_assignation'),
        path('<int:team_id>/', include([
            path('', views.team_page_view, name='team_page_view'),
            path('add_project/', views.add_project_view, name='add_project_view'),
            path('projects/<int:project_id>/', include([
                path('', views.project_page_view, name='project_page_view'),
                path('add_task/', views.add_task_view, name='add_task_view'),
                path('tasks/<int:task_id>/', include([
                    path('details/', views.task_details_view, name='task_details'),
                    path('assign_to_me/', views.assign_task_to_me_view, name='assign_task_to_me'),  # Updated
                    path('change_status/', views.change_task_status_view, name='change_task_status'),
                    path('edit/', views.edit_task_view, name='edit_task'),
                    path('delete/', views.delete_task_view, name='delete_task'),
                ])),
            ])),
        ])),
    ])),
]
