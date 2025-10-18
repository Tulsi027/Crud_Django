from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                    # main CRUD page (calls backend API)
    path('register/', views.register, name='register'),   # user registration via backend
    path('login/', views.login_view, name='login'),       # JWT login handled in frontend
    path('logout/', views.logout_view, name='logout'),    # clears JWT tokens & session
]
