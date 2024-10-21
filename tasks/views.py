from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import User, Task
# signals.py
from django.contrib.auth.decorators import login_required

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, Notification

from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

@receiver(post_save, sender=Task)
def create_notification(sender, instance, created, **kwargs):
    if created:
        users_to_notify = User.objects.exclude(id=instance.created_by.id)  
        for user in users_to_notify:
            Notification.objects.create(task=instance, user=user)



def user_register(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        privileges = request.POST.get('privileges')
        
        if User.objects.filter(user_id=user_id).exists():
            messages.error(request, 'User  ID already exists!')
        else:
            hashed_password = make_password(password)  # Hash the password
            User.objects.create(user_id=user_id, password=hashed_password, privileges=privileges)
            messages.success(request, 'User  registered successfully!')
            return redirect('login') 

    return render(request, 'register.html')



def user_login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        try:
            user = User.objects.get(user_id=user_id)
            if check_password(password, user.password):  # Check the hashed password
                request.session['user_id'] = user.user_id
                request.session['privileges'] = user.privileges
                messages.success(request, 'Login successful!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid user ID or password!')
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Invalid user ID or password!')
            return redirect('login')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')

    privileges = request.session.get('privileges')

    if privileges == 'admin':
        tasks = Task.objects.all() 
    else:
        tasks = Task.objects.filter(is_completed=False)

    notifications = Notification.objects.filter(user__user_id=request.session['user_id'], seen=False)

    context = {
        'tasks': tasks,
        'privileges': privileges,
        'notifications': notifications,  # Include notifications in the context
    }

    return render(request, 'dashboard.html', context)

def create_task(request):
    if request.method == 'POST':
        if 'user_id' not in request.session:
            return HttpResponse('Unauthorized', status=401)

        task_name = request.POST.get('task_name')
        due_date = request.POST.get('due_date')

        user_id = request.session['user_id']
        user = User.objects.get(user_id=user_id)

        Task.objects.create(task_name=task_name, due_date=due_date, is_completed=False, created_by=user)
        
        messages.success(request, f'Task "{task_name}" created successfully!')

        return redirect('dashboard')

    return HttpResponse('Invalid request method', status=405)
