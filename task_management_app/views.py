from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import Task, User, Comment
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import send_update_mail, send_update_status
from .forms import (
    UserCreateForm,
    TaskUpdateForm,
    TaskCreateForm,
    LoginForm,
    RegistrationForm,
    CommentForm,
)


# user login user With email and password
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("homepage")
            else:
                messages.error(
                    request,
                    "Authentication failed. Please check your credentials.",
                )
        else:
            messages.error(request, "Please fill out the form correctly.")
        return render(request, "login.html", {"form": form})


# create new user
class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "registration.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            phone_no = form.cleaned_data.get("phone_no")
            password = form.cleaned_data.get("password")

            user = User.objects.create_user(
                email=email, phone_no=phone_no, password=password
            )
            user.save()

            messages.success(request, "User registered successfully")
            return redirect("loginform")
        else:
            messages.error(request, "Please correct the errors below.")
        return render(request, "registration.html", {"form": form})


# home page with task list
class HomePage(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.is_superuser:
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(
                Q(assigned_by=user) | Q(assigned_to=user)
            )

        total = tasks.count()
        completed_tasks = tasks.filter(status="completed")
        completed_count = completed_tasks.count()
        in_progress_tasks = tasks.filter(status="in_progress")
        in_progress_count = in_progress_tasks.count()
        pending_tasks = tasks.filter(status="pending")
        pending_count = pending_tasks.count()

        return render(
            request,
            "home.html" if user.is_superuser else "homepage.html",
            {
                "tasks": tasks,
                "total": total,
                "completed_count": completed_count,
                "in_progress_count": in_progress_count,
                "pending_count": pending_count,
                "completed_tasks": completed_tasks,
                "in_progress_tasks": in_progress_tasks,
                "pending_tasks": pending_tasks,
            },
        )


# logout user
class LogoutPage(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("loginform")


# user profile show
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        try:
            profile = get_object_or_404(User, email=user.email)
            return render(
                request, "userprofile.html", {"profile": profile, "user": user}
            )
        except User.DoesNotExist:
            return HttpResponse("Profile not found", status=404)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)


# create new task
class TaskCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = TaskCreateForm()
        return render(request, "taskcreateform.html", {"form": form})

    def post(self, request):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            send_update_mail(task)
            messages.success(request, "Task created successfully")
            return redirect("homepage")
        else:
            messages.error(request, "There was an error creating the task.")
        return render(request, "taskcreateform.html", {"form": form})


# task list show
class TaskView(LoginRequiredMixin, View):
    def get(self, request):
        Tasks = Task.objects.all()
        return render(
            request,
            "tasklist.html",
            {
                "tasks": Tasks,
            },
        )


# show details of perticular view
class TaskDetails(LoginRequiredMixin, View):
    def get(self, request, id):
        task = get_object_or_404(Task, id=id)
        return render(request, "taskdetails.html", {"task": task})


# create comment for perticular task
class CommentView(View):
    def get(self, request, id):
        form = CommentForm()
        task = get_object_or_404(Task, id=id)
        return render(
            request, "commentform.html", {"form": form, "task": task}
        )

    def post(self, request, id):
        form = CommentForm(request.POST)
        task = get_object_or_404(Task, id=id)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user_reference = request.user
            comment.task_reference = task
            comment.save()
            messages.success(request, "Comment added successfully")
            return redirect(f"/CommentShow/{id}")
        else:
            messages.error(request, "Please correct the errors below.")
        return render(
            request, "commentform.html", {"form": form, "task": task}
        )


# dalete Task
class DeleteTask(LoginRequiredMixin, View):
    def get(self, request, id):
        task = Task.objects.filter(id=id)
        task.delete()
        return redirect("TaskView")


# Task data update
class TaskUpdateView(LoginRequiredMixin, View):
    def get(self, request, id):
        task = get_object_or_404(Task, pk=id)
        form = TaskUpdateForm(instance=task)
        return render(request, "updateform.html", {"form": form, "task": task})

    def post(self, request, id):
        task = get_object_or_404(Task, pk=id)
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            task.save()
            send_update_status(task)
            messages.success(request, "Task updated successfully")
            return redirect("homepage")
        else:
            messages.error(request, "There was an error updating the task.")
        return render(request, "updateform.html", {"form": form, "task": task})


# show comment for perticular Task
class CommentShow(LoginRequiredMixin, View):
    def get(self, request, id):
        task = Task.objects.get(id=id)
        comments = Comment.objects.filter(task_reference=task).order_by(
            "-created_at"
        )
        num = comments.count()
        if num == 1:
            comment = comments.first()
            return render(request, "commentshow.html", {"comment": comment})
        else:
            return render(request, "commentshow.html", {"comments": comments})


# create new user
class UserCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = UserCreateForm()
        return render(request, "usercreate.html", {"form": form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User Created Successfully")
            return redirect("homepage")
        else:
            messages.error(request, "There was an error creating the user.")
        return render(request, "usercreate.html", {"form": form})


# show user List
class UserList(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.all()
        return render(request, "userlist.html", {"users": users})


# Search task with title,enddate,status
class TaskSearch(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get("q", "").strip()
        if query:
            try:
                tasks = Task.objects.filter(
                    Q(title__icontains=query)
                    | Q(end_date__icontains=query)
                    | Q(status__icontains=query)
                )
            except Exception:
                tasks = Task.objects.all()
        else:
            tasks = Task.objects.all()

        return render(request, "search.html", {"tasks": tasks, "query": query})
