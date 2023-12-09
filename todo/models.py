from django.contrib.auth.models import User
from django.db import models


class Todo(models.Model):
    """
    Model representing a Todo item.

    Attributes:
        title (CharField): The title of the Todo item.
        memo (TextField): The memo or description of the Todo item.
        created (DateTimeField): The date and time when the Todo item was created.
        datecompleted (DateTimeField): The date and time when the Todo item was completed.
        important (BooleanField): Indicates whether the Todo item is important or not.
        user (ForeignKey): The user associated with the Todo item.

    Methods:
        __str__(): Returns a string representation of the Todo item.

    """

    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
