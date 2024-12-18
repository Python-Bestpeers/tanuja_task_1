from django import forms
from .models import User, Task, Comment, SubTask


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "phone_no"]


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "priority", "status", "end_date", "description"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Enter task title"}
            ),
            "priority": forms.Select(),
            "status": forms.Select(),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(
                attrs={"placeholder": "Enter task description"}
            ),
        }


class TaskCreateForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={"class": "form-select", "id": "assign_to"}),
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "priority",
            "status",
            "end_date",
            "assigned_to",
            "description",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "task-name",
                    "placeholder": "Enter task name",
                }
            ),
            "priority": forms.Select(
                attrs={"class": "form-select", "id": "priority"}
            ),
            "status": forms.Select(
                attrs={"class": "form-select", "id": "status"}
            ),
            "end_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "id": "end-date",
                    "type": "date",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "id": "description",
                    "placeholder": "Enter task description",
                    "rows": 5,
                    "cols": 30,
                }
            ),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "required": "required",
                "class": "form-control",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "required": "required",
                "class": "form-control",
            }
        )
    )


class RegistrationForm(forms.ModelForm):
    
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter your email",
                "required": "required",
                "class": "form-control",
            }
        )
    )
    phone_no = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Enter your contact number",
                "required": "required",
                "class": "form-control",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Create password",
                "required": "required",
                "class": "form-control",
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm password",
                "required": "required",
                "class": "form-control",
            }
        )
    )
    terms = forms.BooleanField(required=True, widget=forms.CheckboxInput())
    
    class Meta:
        model = User
        fields=['email', 'phone_no', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_text"]
        widgets = {
            "comment_text": forms.Textarea(
                attrs={
                    "id": "comment_text",
                    "placeholder": "Write your comment here...",
                    "required": "required",
                    "class": "form-control",
                }
            )
        }


class SubTaskCreateForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ["title", "status", "assigned_to"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Sub-task Title",
                }
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "assigned_to": forms.Select(attrs={"class": "form-select"}),
        }


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ["title", "status", "parent_task"]

    STATUS_CHOICES = [
        ("completed", "completed"),
        ("in-progress", "in-progress"),
        ("pending", "pending"),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES)
