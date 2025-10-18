from django.shortcuts import render, redirect
from django.contrib import messages
import requests

# 🔗 Backend API URLs
BACKEND_API_URL = "http://127.0.0.1:8001/api/students/"
BACKEND_TOKEN_URL = "http://127.0.0.1:8001/api/token/"
BACKEND_REGISTER_URL = "http://127.0.0.1:8001/api/register/"

# 🏠 Home view (CRUD via backend API using JWT token)
def home(request):
    # ✅ Get JWT token from session
    access_token = request.session.get('access_token')

    if not access_token:
        messages.error(request, "Please log in first!")
        return redirect('login')

    headers = {"Authorization": f"Bearer {access_token}"}
    search_query = ""
    students = []

    # ✅ Fetch all students from backend API
    response = requests.get(BACKEND_API_URL, headers=headers)
    if response.status_code == 200:
        students = response.json()
    elif response.status_code == 401:
        # Token expired or invalid
        messages.error(request, "Session expired! Please log in again.")
        return redirect('login')
    else:
        messages.error(request, "Error fetching data from backend")

    if request.method == "POST":
        if "search" in request.POST:
            search_query = request.POST.get("query", "")
            students = [s for s in students if search_query.lower() in s['name'].lower()]

        elif "create" in request.POST:
            name = request.POST.get("name")
            email = request.POST.get("email")
            data = {"name": name, "email": email}
            res = requests.post(BACKEND_API_URL, headers=headers, json=data)
            if res.status_code == 201:
                messages.success(request, "Student added successfully!")
            else:
                messages.error(request, f"Error adding student! ({res.status_code})")
            return redirect('home')

        elif "update" in request.POST:
            student_id = request.POST.get("id")
            name = request.POST.get("name")
            email = request.POST.get("email")
            data = {"name": name, "email": email}
            res = requests.put(f"{BACKEND_API_URL}{student_id}/", headers=headers, json=data)
            if res.status_code == 200:
                messages.success(request, "Student updated successfully!")
            else:
                messages.error(request, f"Error updating student! ({res.status_code})")
            return redirect('home')

        elif "delete" in request.POST:
            student_id = request.POST.get("id")
            res = requests.delete(f"{BACKEND_API_URL}{student_id}/", headers=headers)
            if res.status_code in [200, 204]:
                messages.success(request, "Student deleted successfully!")
            else:
                messages.error(request, f"Error deleting student! ({res.status_code})")
            return redirect('home')

    context = {"students": students, "search_query": search_query}
    return render(request, 'index.html', context)


# 👤 Register view (handled via backend)
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:
            messages.error(request, "Passwords do not match!")
        else:
            data = {"username": username, "password": password}
            response = requests.post(BACKEND_REGISTER_URL, json=data)

            if response.status_code == 201:
                messages.success(request, "Account created successfully!")
                return redirect('login')
            else:
                messages.error(request, f"Error creating account! ({response.status_code})")

    return render(request, 'register.html')


# 🔑 Login view — fetch JWT tokens from backend
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        data = {"username": username, "password": password}
        response = requests.post(BACKEND_TOKEN_URL, json=data)

        if response.status_code == 200:
            tokens = response.json()
            # ✅ Save access + refresh tokens in session
            request.session['access_token'] = tokens['access']
            request.session['refresh_token'] = tokens['refresh']
            request.session['username'] = username
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


# 🚪 Logout view
def logout_view(request):
    request.session.flush()  # clear tokens and user info
    messages.success(request, "Logged out successfully!")
    return redirect('login')
