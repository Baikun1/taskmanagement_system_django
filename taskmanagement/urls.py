"""
URL configuration for taskmanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard,name='dashboard'),
    path('login/', user_login,name='login'),
    path('logout/', user_logout,name='logout'),    
    path('register/', user_register,name='register'),   
    path('create-task/',create_task, name='create_task'), 


]
