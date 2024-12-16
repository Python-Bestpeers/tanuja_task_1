from django.urls import path
from .views import (
    LoginForm,
    SignupForm,
    HomePage,
    LogoutPage,
    ProfileView,
    TaskCreate,
    TaskView,
    TaskDetails,
    CommentData,
    DeleteTask,
    UpdateTask,
    CommentShow,
    UserCreate,
    UserList,
    TaskSearch,
)


urlpatterns = [
    path("", LoginForm.as_view(), name="loginform"),
    path("signupform/", SignupForm.as_view(), name="signupform"),
    path("homepage/", HomePage.as_view(), name="homepage"),
    # path('userhome/',userhome.as_view(),name="userhome"),
    path("logoutpage/", LogoutPage.as_view(), name="logoutpage"),
    path("Profileview/", ProfileView.as_view(), name="profileview"),
    path("TaskCreate/", TaskCreate.as_view(), name="TaskCreate"),
    path("TaskView/", TaskView.as_view(), name="TaskView"),
    path("Taskdetails/<int:id>", TaskDetails.as_view(), name="Taskdetails"),
    path("DeleteTask/<int:id>", DeleteTask.as_view(), name="DeleteTask"),
    path("Commentdata/<int:id>", CommentData.as_view(), name="Commentdata"),
    path("CommentShow/<int:id>", CommentShow.as_view(), name="CommentShow"),
    path("UpdateTask/<int:id>", UpdateTask.as_view(), name="UpdateTask"),
    path("Usercreate/", UserCreate.as_view(), name="Usercreate"),
    path("UserList/", UserList.as_view(), name="UserList"),
    path("TaskSearch/", TaskSearch.as_view(), name="TaskSearch"),
]
