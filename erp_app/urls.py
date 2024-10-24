from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth_view, name='auth'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('groups/', views.group_list_view, name='group_list'),
    path('groups/create/', views.group_create_view, name='group_create'),
    path('groups/assign/', views.assign_users_to_group_view, name='assign_users_to_group'),
]
