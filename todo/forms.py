from django.forms import ModelForm

from .models import Todo


class TodoForm(ModelForm):
    """
    Form for creating or updating a Todo.

    Args:
        self: The TodoForm instance.

    Attributes:
        Meta (class): Inner class that defines the metadata options for the form.
            - model (Model): The model class associated with the form.
            - fields (list): The fields to include in the form.

    """

    class Meta:
        model = Todo
        fields = ["title", "memo", "important"]
