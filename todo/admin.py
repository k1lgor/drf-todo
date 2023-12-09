from django.contrib import admin

from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    """
    Admin model for Todo.

    Args:
        self: The TodoAdmin instance.

    Attributes:
        readonly_fields (tuple): Fields that are read-only in the admin interface.

    """

    readonly_fields = ("created",)


admin.site.register(Todo, TodoAdmin)
