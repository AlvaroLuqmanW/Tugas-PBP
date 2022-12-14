from multiprocessing import context
import re
from urllib import response
from django.shortcuts import render
from todolist.models import Task
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import TaskForm
from .forms import CustomUserCreationForm  
import datetime


# Create your views here.
@login_required(login_url='/todolist/login/')

def show_todolist(request): 
    form = TaskForm(request.POST)   

    data_task = Task.objects.all()
    context = {
        'task': data_task,
        'last_login': request.COOKIES['last_login'],
        'user': request.user,
        'form': form
    }
    return render(request, 'todolist.html', context)

def show_createtask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)  
   
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            user = request.user
            task_temp = tambah_task(title, description, user)
            task_temp.save()
        return HttpResponseRedirect("/todolist/" )
    else:
        form = TaskForm()
    context = {'form': form}
    return render(request, 'create-task.html', context)

def addtask(request):
    title = title
    description = description
    user = request.user
    task_temp = tambah_task(title, description, user)
    task_temp.save()
    return render(request, 'add.html')

def register(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('todolist:login')
        else:  
            form = CustomUserCreationForm()  
    
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("todolist:show_todolist")) # membuat response
            response.set_cookie('last_login', str(datetime.datetime.now())) # membuat cookie last_login dan menambahkannya ke dalam response
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('todolist:login'))
    response.delete_cookie('last_login')
    return response

def show_json(request):
    data_task = Task.objects.all()
    context = {
        'task': data_task,
        'last_login': request.COOKIES['last_login'],
        'user': request.user,
    }
    return render(request, 'todolist-json.html', context)    

def tambah_task(title, description, user):
    return Task.objects.create(title=title, description=description, user = user)

