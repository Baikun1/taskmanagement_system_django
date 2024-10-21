from django.contrib import admin

# Register your models here.
from .models import User, Task ,Notification

# Registering the models
admin.site.register(User)
admin.site.register(Task)
admin.site.register(Notification)
