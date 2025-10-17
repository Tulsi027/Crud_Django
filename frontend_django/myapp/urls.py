from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from myapp import views

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # main page that calls backend API
    path('register/', views.register, name='register'),

    # Authentication routes
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
