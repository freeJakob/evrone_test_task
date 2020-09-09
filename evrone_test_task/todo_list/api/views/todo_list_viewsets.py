from rest_framework import viewsets, filters
from rest_framework.serializers import ModelSerializer

from todo_list.api.serializers.todo_list_serializers import (
    ToDoListRetrieveSerializer,
    ToDoListCreateSerializer,
    ToDoListUpdateSerializer,
)
from todo_list.models import ToDoList


class ToDoListViewSet(viewsets.ModelViewSet):
    queryset = ToDoList.objects.all()
    serializers = {
        'retrieve': ToDoListRetrieveSerializer,
        'update': ToDoListUpdateSerializer,
        'partial_update': ToDoListUpdateSerializer,
        'create': ToDoListCreateSerializer,
        'default': ToDoListRetrieveSerializer
    }
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = ['title']

    def get_serializer_class(self) -> ModelSerializer:
        serializer_class = self.serializers.get(
            self.action,
            self.serializers.get('default'),
        )

        return serializer_class
