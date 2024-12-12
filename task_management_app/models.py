import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from .manager import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group,Permission



class Timestampmodel(models.Model):
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    
    class Meta:
        abstract = True


class User(AbstractUser, Timestampmodel):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_no = models.CharField(max_length=15, unique=True, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    def __str__(self):
        return self.email


class Task(Timestampmodel):
    PRIORITY_CHOICES = (
        ("high", "high"),
        ("medium", "medium"),
        ("low", "low"),
    )
    STATUS_CHOICES = (
        ("pending", "pending"),
        ("in-progress", "in-progress"),
        ("completed", "completed"),
    )
    title = models.CharField(max_length=100)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_tasks",null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    description = models.TextField(default="")

    def __str__(self):
        return self.title


class Comment(Timestampmodel):
    comment_text = models.CharField(max_length=400)
    task_reference = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    user_reference = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")

    def __str__(self):
        return self.comment_text

