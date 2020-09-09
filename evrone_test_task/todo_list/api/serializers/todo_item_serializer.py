from rest_framework import serializers

from todo_list.models import ToDoItem


class ToDoItemRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoItem
        fields = ('id', 'title', 'description', 'todo_list')


class ToDoItemCreateSerializer(serializers.ModelSerializer):
    todo_list_id = serializers.IntegerField()

    class Meta:
        model = ToDoItem
        fields = ('title', 'description', 'todo_list_id', 'pk')


class ToDoItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoItem
        fields = ('title', 'description', 'pk')
