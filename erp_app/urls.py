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
]
