import factory

from todo_list.models import ToDoList
from todo_list.test_factories.todo_item_factories import ToDoItemFactory


class ToDoListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ToDoList

    title = factory.Sequence(lambda n: 'ToDo List title %d' % n)
    todo_items = factory.RelatedFactory(
        ToDoItemFactory,
        factory_related_name='todo_list',
    )