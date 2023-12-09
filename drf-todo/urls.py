"""drf-todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from todo import views

urlpatterns = [
    # Admin panel
    path("admin/", admin.site.urls),
    # User authentication
    path("signup/", views.signupuser, name="signupuser"),  # User signup
    path("login/", views.loginuser, name="loginuser"),  # User login
    path("logout/", views.logoutuser, name="logoutuser"),  # User logout
    # Todo operations
    path("", views.home, name="home"),  # Home page
    path("create/", views.createtodo, name="createtodo"),  # Create a new todo
    path("current/", views.currenttodos, name="currenttodos"),  # View current todos
    path(
        "completed/", views.completedtodos, name="completedtodos"
    ),  # View completed todos
    path("todo/<int:todo_pk>", views.viewtodo, name="viewtodo"),  # View a specific todo
    path(
        "todo/<int:todo_pk>/complete", views.completetodo, name="completetodo"
    ),  # Mark a todo as complete
    path(
        "todo/<int:todo_pk>/delete", views.deletetodo, name="deletetodo"
    ),  # Delete a todo
    # API
    path("api/", include("api.urls")),  # API endpoints
]
