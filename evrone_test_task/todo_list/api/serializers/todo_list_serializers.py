from rest_framework import serializers

from todo_list.api.serializers.todo_item_serializer import (
    ToDoItemRetrieveSerializer,
)
from todo_list.models import ToDoList


class ToDoListRetrieveSerializer(serializers.ModelSerializer):
    todo_items = ToDoItemRetrieveSerializer(many=True)

    class Meta:
        model = ToDoList
        fields = ('id', 'title', 'created', 'todo_items')


class ToDoListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = ('title', 'pk')


class ToDoListUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = ('title', 'pk')
