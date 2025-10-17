from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests  # ✅ for API calls

# 🔗 Backend API endpoint
BACKEND_API_URL = "http://127.0.0.1:8001/api/students/"

# 🏠 Home view (CRUD via backend API)
@login_required(login_url='/login/')
def home(request):
    search_query = ""
    students = []

    # ✅ Fetch all students from backend
    response = requests.get(BACKEND_API_URL)
    if response.status_code == 200:
        students = response.json()

    if request.method == "POST":
        if "search" in request.POST:
            search_query = request.POST.get("query", "")
            # Optional: simple client-side filtering
            students = [s for s in students if search_query.lower() in s['name'].lower()]

        elif "create" in request.POST:
            name = request.POST.get("name")
            email = request.POST.get("email")
            data = {"name": name, "email": email}
            res = requests.post(BACKEND_API_URL, data=data)
            if res.status_code == 201:
                messages.success(request, "Student added successfully!")
            else:
                messages.error(request, "Error adding student!")
            return redirect('home')

        elif "update" in request.POST:
            student_id = request.POST.get("id")
            name = request.POST.get("name")
            email = request.POST.get("email")
            data = {"name": name, "email": email}
            res = requests.put(f"{BACKEND_API_URL}{student_id}/", data=data)
            if res.status_code == 200:
                messages.success(request, "Student updated successfully!")
            else:
                messages.error(request, "Error updating student!")
            return redirect('home')

        elif "delete" in request.POST:
            student_id = request.POST.get("id")
            res = requests.delete(f"{BACKEND_API_URL}{student_id}/")
            if res.status_code in [200, 204]:
                messages.success(request, "Student deleted successfully!")
            else:
                messages.error(request, "Error deleting student!")
            return redirect('home')

    context = {"students": students, "search_query": search_query}
    return render(request, 'index.html', context)


# 👤 Register view (same as before)
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:
            messages.error(request, "Passwords do not match!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')

    return render(request, 'register.html')
