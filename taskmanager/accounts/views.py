from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from tasks.models import Task
from accounts.models import User
from datetime import datetime
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import PermissionDenied
from .forms import AssignAdminForm
from django.shortcuts import render, get_object_or_404, redirect

def admin_login(request):
    print("----------")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.groups.filter(name__in=['Admin', 'SuperAdmin']).exists():
            login(request, user)
            return redirect('dashboard')
    return render(request, 'custom_admin_panel/login.html')


@login_required()
def dashboard(request):
    if request.user.role == 'SuperAdmin':
        tasks = Task.objects.all()
        users = User.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to__assigned_admin=request.user)
        users = User.objects.filter(assigned_admin=request.user)
    return render(request, 'custom_admin_panel/dashboard.html', {
        'tasks': tasks,
        'users': users
    })

def task_list(request):
    tasks = Task.objects.all()
    return render(request, "custom_admin_panel/task_list.html", {"tasks": tasks})
@login_required
def create_task(request):
    if not request.user.groups.filter(name="Admin").exists():
        return redirect("dashboard")
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        due_date = request.POST["due_date"]
        user_id = request.POST["assigned_to"]
        user = User.objects.get(id=user_id)
        if user.assigned_admin != request.user:
            return redirect("dashboard")

        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            assigned_to=user
        )
        return redirect("dashboard")
    users = User.objects.filter(assigned_admin=request.user)
    return render(request, "custom_admin_panel/create_task.html", {"users": users})
@login_required
def delete_task(request, id):
    task = Task.objects.get(id=id)
    if request.user.is_superuser:
        task.delete()

    elif request.user.groups.filter(name="Admin").exists():
        if task.assigned_to.assigned_admin == request.user:
            task.delete()

    return redirect("dashboard")


@login_required
def user_list(request):
    if not request.user.is_superuser:
        return redirect("dashboard")
    users = User.objects.all()
    return render(request, "custom_admin_panel/user_list.html", {"users": users})

@login_required
def create_user(request):
    if not request.user.is_superuser:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        role = request.POST["role"]
        user = User.objects.create_user(username=username,email=email,password=password,role=role)
        group = Group.objects.get(name=role)
        print(group)
        user.groups.add(group)
        return redirect("user_list")
 
    return render(request, "custom_admin_panel/create_user.html")

@login_required
def promote_to_admin(request, id):
    print(request.user.is_superuser)
    if not request.user.is_superuser:
        return redirect("dashboard")

    user = User.objects.get(id=id)
    admin_group = Group.objects.get(name="Admin")
    user.groups.clear()
    user.groups.add(admin_group)
    return redirect("user_list")
@login_required
def demote_to_user(request, id):
    if not request.user.is_superuser:
        return redirect("dashboard")
    user = User.objects.get(id=id)
    user_group = Group.objects.get(name="User")
    user.groups.clear()
    user.groups.add(user_group)
    return redirect("user_list")
@login_required
def delete_user(request, id):
    if not request.user.is_superuser:
        return redirect("dashboard")
    user = User.objects.get(id=id)
    user.delete()
    return redirect("user_list")

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required
def assign_admin_view(request):
    if request.user.role != 'SuperAdmin':
        raise PermissionDenied("Only superadmin can assign admins.")
    if request.method == "POST":
        form = AssignAdminForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            admin = form.cleaned_data['admin']
            user.assigned_admin = admin
            user.save()
            return redirect('user_list') 
    else:
        form = AssignAdminForm()
    return render(request, "custom_admin_panel/assign_admin.html", {"form": form})

@login_required
def user_admin_list_view(request,uuid):
    if request.user.role != "SuperAdmin":
        raise PermissionDenied("Only superadmin can view this page.")
    users = User.objects.filter(role='User',assigned_admin=uuid).select_related('assigned_admin')
    return render(
        request,
        "custom_admin_panel/user_admin_list.html",
        {"users": users}
    )


def assign_role(request, uuid):
    if request.user.role != 'SuperAdmin':
        return redirect('dashboard')
    user = get_object_or_404(User, id=uuid)
    if request.method == "POST":
        new_role = request.POST.get("role")
        if new_role in ['SuperAdmin', 'Admin', 'User']:
            user.role = new_role
            user.groups.clear()
            group = Group.objects.get(name=new_role)
            user.groups.add(group)
            if new_role == 'Admin':
                user.assigned_admin = None
            user.save()
        return redirect('user_list')

    return render(request, "custom_admin_panel/assign_role.html", {
        "target_user": user
    })
