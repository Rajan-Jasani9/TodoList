from django.urls import path
from .views import TaskCreate, TaskDetail, TaskList, TaskUpdate, TaskDelete
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('register/',views.RegisterPage.as_view(), name='register'),
    path('login/',views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('',views.TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/',views.TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name="task-create"),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name="task-edit"),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name="task-delete"),
]   