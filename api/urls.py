from django.urls import path

from api import views

urlpatterns = [
    # Todos
    path("todos/completed", views.TodoCompletedList.as_view()),
    path("todos", views.TodoListCreate.as_view()),
    path("todos/<int:pk>", views.TodoRetrieveUpdateDestroy.as_view()),
    path("todos/<int:pk>/complete", views.TodoComplete.as_view()),
    # Auth
    path("signup", views.signup),
    path("signup", views.login),
]
