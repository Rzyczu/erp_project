from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth_view, name='auth'),
    path('registration/', views.registration_view, name='registration'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

]
