from django.shortcuts import render,redirect
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from .models import Task, User, Comment
from .models import User
from django.contrib import messages
from django.views import View
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
import datetime

# Create your views here.
User = get_user_model()
class loginform(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('Password')

        if not email or not password:
            messages.error(request, "Email aur password zaruri hai.")
            return redirect('loginform')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage') 
        else:
            messages.error(request, "Authentication failed. Please check your credentials.")
            return redirect("loginform")


class signupform(View):
  def get(self,request):
    return render(request,'registration.html')
  def post(self,request):
      email = request.POST.get("email")
      phone_no=request.POST.get("phone_no")
      password = request.POST.get("password")
      confirm_password = request.POST.get("confirm_password")
       
      if password != confirm_password:
        print("hello")
        messages.error(request, "Passwords do not match!")
        return redirect("signupform")

      if User.objects.filter(email=email).exists():
        print("hello1")
        messages.error(request, "Email is already registered.")
        return redirect("signupform")

      if User.objects.filter(phone_no=phone_no).exists():
        print("hello2")
        messages.error(request, "Phone number is already registered.")
        return redirect("signupform")
      
      user = User.objects.create_user(email=email, phone_no=phone_no, password=password)
      print(user)
      login(request, user)
      return redirect("loginform")  
  
class Homepage(View):
  def get(self,request):
    user=request.user
    if user.is_superuser:
      tasks=Task.objects.all()
      total=tasks.count()
      completed = tasks.filter(status="completed").count() 
      print(completed)
      in_progress = tasks.filter(status="in_progress").count() 
      print(in_progress)
      pending = tasks.filter(status="pending").count()
      print(pending)
      return render(request, "home.html",{'tasks':tasks,'total':total,'completed':completed,'in_progress':in_progress,'pending':pending})
    else:
      tasks=Task.objects.all()
      total=tasks.count()
      completed = tasks.filter(status="completed").count() 
      print(completed)
      in_progress = tasks.filter(status="in_progress").count() 
      print(in_progress)
      pending = tasks.filter(status="pending").count()
      print(pending)
      return render(request, "homepage.html",{'tasks':tasks,'total':total,'completed':completed,'in_progress':in_progress,'pending':pending})
      
   
class LogoutPage(View):
  def get(self,request):
        logout(request)
        return redirect('loginform')
    
class Profileview(View):
  def get(self,request):
      user=request.user
      try:
        profile=get_object_or_404(User,email=user.email)
        print(profile.email)
        print(profile.phone_no)
        return render(request,'userprofile.html',{'profile':profile,'user':user})
      except User.DoesNotExist:
        return HttpResponse("Profile not found", status=404)
      except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

class TaskCreate(View):
    def get(self, request):
        user = request.user
        return render(request, 'taskcreateform.html', {'user': user})

    def post(self, request):
        print("hello users")
        user=request.user
        taskname = request.POST.get('taskname')
        priority = request.POST.get('priority')
        status = request.POST.get('status')
        enddate = request.POST.get('enddate')
        assigner = request.user
        print(assigner)
        assignee_email = request.POST.get('assignee')
        description = request.POST.get('description')

        try:
            user1 = User.objects.get(email=assignee_email.strip().lower())
            print(user1)
        except User.DoesNotExist:
            return render(request, 'taskcreateform.html', {
                'user': assigner,
                'error': f"No user found with email {assignee_email}",
            })

        Task.objects.create(
            title=taskname,
            priority=priority,
            status=status,
            assigned_by=assigner,
            assigned_to=user1,
            end_date=enddate,
            description=description,
        )
        subject='Task Assigned'
        message=f'''Task : {taskname},
                    Description: {description},
                    Assigned_By:{assigner}
                    Priority: {priority}
                    Start Date: {datetime.datetime.now},
                    End Date: {enddate}
            '''
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [assignee_email]     
        send_mail(subject, message, email_from, recipient_list)

        return redirect('homepage')



class TaskView(View):
  def get(self,request):
      print("hello")
      user=request.user
      Tasks=Task.objects.all()
      return render(request, 'tasklist.html', {
                'tasks': Tasks,
      })


class Taskdetails(View):
   def get(self,request,id):
      task = get_object_or_404(Task, id=id) 
      return render(request,'taskdetails.html',{'task':task})
    
class Commentdata(View):
  def get(self,request,id):
    user=request.user
    task=Task.objects.get(id=id)
    return render(request,'commentform.html',{'task':task})
  def post(self,request,id): 
    text=request.POST.get('commentdata')
    task=Task.objects.get(id=id)
    if text:
      Comment.objects.create(user_reference=request.user,comment_text=text,task_reference=task)
      messages.success(request,"comment added successfully")
      return redirect(f'/CommentShow/{id}')  
    else:
      messages.error(request,"task comment is not found")
      return redirect('Taskdetails')
    
class DeleteTask(View):
  def get(self,request,id):
    task=Task.objects.filter(id=id)
    task.delete()
    return redirect('TaskView')
  
class UpdateTask(View):
  def get(self,request,id):
    user=request.user
    task=Task.objects.filter(id=id).values().first()
    if task:
      task['start_date'] = task['start_date'].strftime('%Y-%m-%d')
      task['end_date'] = task['end_date'].strftime('%Y-%m-%d')
    print(task)
    return render(request,'updateform.html',{'task':task})
  def post(self,request,id):
    user=request.user
    task=get_object_or_404(Task,id=id)
    
    task.title=request.POST.get('title')
    task.priority=request.POST.get('priority')
    task.status=request.POST.get('status')
    task.end_date=request.POST.get('end_date')
    task.description=request.POST.get('description')
    task.save()
    subject='Task Status Update'
    message=f'''Task : {task.title},
                    Description: {task.description},
                    Assigned_By:{task.assigned_by}
                    Priority: {task.priority}
                    Start Date: {task.start_date},
                    End Date: {task.end_date}
            '''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [task.assigned_to]     
    send_mail(subject, message, email_from, recipient_list)

    messages.success(request,"task updated Succefully")
    return redirect("homepage")    
    
   

class CommentShow(View):
  def get(self,request,id):
    task=Task.objects.get(id=id)
    comments=Comment.objects.filter(task_reference=task).order_by('-created_at')
    num=comments.count()
    if num==1:
      comment=comments.first()
      return render(request,'commentshow.html',{'comment':comment})
    else:
      return render(request,'commentshow.html',{'comments':comments})
    
class Usercreate(View):
  def get(self,request):
    return render(request,'usercreate.html')
  
  def post(self,request):
    user=request.user
    user=User.objects.all()
    email=request.POST.get('email')
    phone_no=request.POST.get('phone')
    User.objects.create_user(email=email,phone_no=phone_no)
    messages.success(request,"User Craeted Successully")
    return redirect('homepage')
  
class UserList(View):
  def get(self,request):
    users=User.objects.all()
    return render(request,'userlist.html',{'users':users})
  
class TaskSearch(View):
    def get(self,request):
        query = request.GET.get('q','')
        print(query)
        if query:
           
          tasks = Task.objects.filter(
                Q(title__icontains=query) |
                Q(end_date=query) |
                Q(status=query)
          )
          print(tasks)
        else:
            tasks = Task.objects.all()
        return render(request, 'search.html', {'tasks': tasks, 'query': query})
    
    

    
    
    
    
    
    
  
    
    


