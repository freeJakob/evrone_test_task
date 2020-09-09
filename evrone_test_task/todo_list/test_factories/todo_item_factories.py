import factory

from todo_list.models import ToDoItem, ToDoList


class ToDoItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ToDoItem

    title = factory.Sequence(lambda n: 'ToDo List title %d' % n)
    description = factory.Sequence(lambda n: 'ToDo List description %d' % n)
