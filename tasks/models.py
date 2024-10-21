from django.db import models

# User Model
class User(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    privileges = models.CharField(max_length=50)

    def __str__(self):
        return self.user_id

# Task Model
# Example of Task model
class Task(models.Model):
    task_name = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  

    def __str__(self):
        return self.task_name
class Notification(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)