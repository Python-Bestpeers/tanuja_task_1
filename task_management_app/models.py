from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_no = models.CharField(
        max_length=15, unique=True, blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Task(TimeStampedModel):
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
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks"
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_tasks",
        null=True,
    )
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    description = models.TextField(default="")

    def __str__(self):
        return self.title


class Comment(TimeStampedModel):
    comment_text = models.CharField(max_length=400)
    task_reference = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="comments"
    )
    user_reference = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments"
    )

    def __str__(self):
        return self.comment_text
