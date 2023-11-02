from django.contrib.auth.models import User
from django.test import TestCase

from todo.models import Todo


class TodoTest(TestCase):
    def test_create_todo_with_all_required_fields(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        todo = Todo(title="Test Todo", user=user)
        assert todo.title == "Test Todo"
        assert todo.memo == ""
        assert todo.datecompleted is None
        assert todo.important is False
        assert todo.user == user

    def test_create_todo_with_only_required_fields(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        todo = Todo(title="Test Todo", user=user)
        assert todo.title == "Test Todo"
        assert todo.memo == ""
        assert todo.datecompleted is None
        assert todo.important is False
        assert todo.user == user

    def test_update_todo_title(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        todo = Todo.objects.create(title="Test Todo", user=user)
        todo.title = "Updated Todo"
        todo.save()
        assert todo.title == "Updated Todo"
