from rest_framework import routers

from todo_list.api.views.todo_item_viewset import ToDoItemViewSet
from todo_list.api.views.todo_list_viewsets import ToDoListViewSet

todo_list_router = routers.SimpleRouter()

todo_list_router.register(
    r'todo_list',
    ToDoListViewSet,
    basename='todo_list',
)
todo_list_router.register(
    r'todo_item',
    ToDoItemViewSet,
    basename='todo_Item',
)
