from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
   path('',loginform.as_view(),name="loginform"),
   path('signupform/',signupform.as_view(),name="signupform"),
   path('homepage/',login_required(Homepage.as_view()),name="homepage"),
   # path('userhome/',login_required(userhome.as_view()),name="userhome"),
   path('logoutpage/',login_required(LogoutPage.as_view()),name="logoutpage"),
   path('Profileview/',login_required(Profileview.as_view()),name="profileview"),
   path('TaskCreate/',login_required(TaskCreate.as_view()),name="TaskCreate"),
   path('TaskView/',login_required(TaskView.as_view()),name="TaskView"),
   path('Taskdetails/<int:id>',login_required(Taskdetails.as_view()),name="Taskdetails"),
   path('DeleteTask/<int:id>',login_required(DeleteTask.as_view()),name="DeleteTask"),
   path('Commentdata/<int:id>',login_required(Commentdata.as_view()),name="Commentdata"),
   path('CommentShow/<int:id>',login_required(CommentShow.as_view()),name="CommentShow"),
   path('UpdateTask/<int:id>',login_required(UpdateTask.as_view()),name="UpdateTask"),
   path('Usercreate/',login_required(Usercreate.as_view()),name="Usercreate"),
   path('UserList/',login_required(UserList.as_view()),name="UserList"),
   path('TaskSearch/',login_required(TaskSearch.as_view()),name="TaskSearch")
]
