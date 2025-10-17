from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student

# Home view (CRUD)
@login_required(login_url='/login/')
def home(request):
    search_query = ""
    students = Student.objects.all()

    if request.method == "POST":
        if "search" in request.POST:
            search_query = request.POST.get("query", "")
            students = students.filter(name__icontains=search_query)
        elif "create" in request.POST:
            name = request.POST.get("name")
            email = request.POST.get("email")
            Student.objects.create(name=name, email=email)
            messages.success(request, "Student added successfully!")
            return redirect('home')
        elif "update" in request.POST:
            student_id = request.POST.get("id")
            student = Student.objects.get(id=student_id)
            student.name = request.POST.get("name")
            student.email = request.POST.get("email")
            student.save()
            messages.success(request, "Student updated successfully!")
            return redirect('home')
        elif "delete" in request.POST:
            student_id = request.POST.get("id")
            Student.objects.get(id=student_id).delete()
            messages.success(request, "Student deleted successfully!")
            return redirect('home')

    context = {"students": students, "search_query": search_query}
    return render(request, 'index.html', context)

# Register view
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
            login(request, user)  # auto login after signup
            messages.success(request, "Account created successfully!")
            return redirect('home')

    return render(request, 'register.html')