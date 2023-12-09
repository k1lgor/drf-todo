from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TodoForm
from .models import Todo


def home(request):
    """
    Render the home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered home page.

    """
    return render(request, "todo/home.html")


def signupuser(request):
    """
    Sign up a new user.

    If the request method is GET, render the signup form.
    If the request method is POST, create a new user with the provided username and password.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered signup form or a redirect to the current todos page.

    Raises:
        IntegrityError: If the username is already taken.

    """
    if request.method == "GET":
        return render(request, "todo/signupuser.html", {"form": UserCreationForm()})
    if request.POST["password1"] != request.POST["password2"]:
        return render(
            request,
            "todo/signupuser.html",
            {"form": UserCreationForm(), "error": "Passwords did not match"},
        )
    try:
        user = User.objects.create_user(
            request.POST["username"], password=request.POST["password1"]
        )
        user.save()
        login(request, user)
        return redirect("currenttodos")
    except IntegrityError:
        return render(
            request,
            "todo/signupuser.html",
            {
                "form": UserCreationForm(),
                "error": "That username has already been taken. Please choose a new username",
            },
        )


def loginuser(request):
    """
    Log in a user.

    If the request method is GET, render the login form.
    If the request method is POST, authenticate the user with the provided username and password.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A redirect to the current todos page if the login is successful.

    """
    if request.method == "GET":
        return render(request, "todo/loginuser.html", {"form": AuthenticationForm()})
    user = authenticate(
        request,
        username=request.POST["username"],
        password=request.POST["password"],
    )
    if user is None:
        return render(
            request,
            "todo/loginuser.html",
            {
                "form": AuthenticationForm(),
                "error": "Username and password did not match",
            },
        )
    login(request, user)
    return redirect("currenttodos")


@login_required
def logoutuser(request):
    """
    Log out the currently authenticated user.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A redirect to the home page.

    """
    if request.method == "POST":
        logout(request)
        return redirect("home")


@login_required
def createtodo(request):
    """
    Create a new Todo.

    If the request method is GET, render the create Todo form.
    If the request method is POST, validate the form data and create a new Todo.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A redirect to the current todos page if the Todo is created successfully.

    Raises:
        ValueError: If the form data is invalid.

    """
    if request.method == "GET":
        return render(request, "todo/createtodo.html", {"form": TodoForm()})
    try:
        form = TodoForm(request.POST)
        newtodo = form.save(commit=False)
        newtodo.user = request.user
        newtodo.save()
        return redirect("currenttodos")
    except ValueError:
        return render(
            request,
            "todo/createtodo.html",
            {"form": TodoForm(), "error": "Bad data passed in. Try again."},
        )


@login_required
def currenttodos(request):
    """
    Render the current todos page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered current todos page.

    """
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "todo/currenttodos.html", {"todos": todos})


@login_required
def completedtodos(request):
    """
    Render the completed todos page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered completed todos page.

    """
    todos = Todo.objects.filter(
        user=request.user, datecompleted__isnull=False
    ).order_by("-datecompleted")
    return render(request, "todo/completedtodos.html", {"todos": todos})


@login_required
def viewtodo(request, todo_pk):
    """
    View and update a specific Todo.

    Args:
        request: The HTTP request object.
        todo_pk (int): The primary key of the Todo to view and update.

    Returns:
        HttpResponse: The rendered viewtodo page or a redirect to the current todos page.

    Raises:
        Http404: If the Todo does not exist or does not belong to the current user.
        ValueError: If the form data is invalid.

    """
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "GET":
        form = TodoForm(instance=todo)
        return render(request, "todo/viewtodo.html", {"todo": todo, "form": form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect("currenttodos")
        except ValueError:
            return render(
                request,
                "todo/viewtodo.html",
                {"todo": todo, "form": form, "error": "Bad info"},
            )


@login_required
def completetodo(request, todo_pk):
    """
    Mark a specific Todo as completed.

    Args:
        request: The HTTP request object.
        todo_pk (int): The primary key of the Todo to mark as completed.

    Returns:
        HttpResponse: A redirect to the current todos page.

    Raises:
        Http404: If the Todo does not exist or does not belong to the current user.

    """
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect("currenttodos")


@login_required
def deletetodo(request, todo_pk):
    """
    Delete a specific Todo.

    Args:
        request: The HTTP request object.
        todo_pk (int): The primary key of the Todo to delete.

    Returns:
        HttpResponse: A redirect to the current todos page.

    Raises:
        Http404: If the Todo does not exist or does not belong to the current user.

    """
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect("currenttodos")
