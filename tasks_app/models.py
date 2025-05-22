from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class TaskUser(AbstractUser):
    full_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=120, unique=True, null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    required_fields = ('full_name', 'email')



class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False, db_index=True)
    author = models.ForeignKey(TaskUser, on_delete=models.CASCADE, related_name='authored_tasks', null=False)
    assignee = models.ForeignKey(TaskUser, on_delete=models.SET_NULL, related_name='assigned_tasks', null=True)
    column = models.ForeignKey('Column', on_delete=models.SET_NULL, null=True)
    sprint = models.ForeignKey('Sprint', on_delete=models.SET_NULL, null=True)
    board = models.ForeignKey('Board', on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True)
    watchers = models.ManyToManyField(TaskUser, related_name='watching_tasks')
    executors = models.ManyToManyField(TaskUser, related_name='executing_tasks')

class Board(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)

class Column(models.Model):
    name = models.CharField(max_length=100, null=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

class Sprint(models.Model):
    name = models.CharField(max_length=100, null=False)
    start_date = models.DateField()
    end_date = models.DateField()

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)

