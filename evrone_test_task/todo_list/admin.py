from django.contrib import admin

# Register your models here.
from todo_list.models import ToDoList, ToDoItem


class ToDoItemInline(admin.StackedInline):
    model = ToDoItem
    extra = 0
    fields = ('title', 'description')


@admin.register(ToDoList)
class ScopeAdmin(admin.ModelAdmin):
    fields = (
        'title',
    )
    list_display = (
        'title',
    )
    inlines = [
        ToDoItemInline,
    ]


@admin.register(ToDoItem)
class ScopeAdmin(admin.ModelAdmin):
    fields = (
        'title', 'description',
    )
    list_display = (
        'pk', 'todo_list_title', 'title', 'description',
    )

    def todo_list_title(self, obj) -> str:
        return obj.todo_list.title
