from django.db import models

# Create your models here.


class ToDoList(models.Model):
    title = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        verbose_name='ToDo List Title',
    )
    created = models.DateTimeField(auto_now_add=True)


class ToDoItem(models.Model):
    todo_list = models.ForeignKey(
        ToDoList,
        on_delete=models.CASCADE,
        related_name='todo_items',
    )
    title = models.CharField(
        blank=False,
        null=False,
        max_length=255,
        verbose_name='ToDo item title',
    )
    description = models.CharField(
        blank=True,
        default='',
        max_length=1024,
        verbose_name='ToDo item description',
    )
