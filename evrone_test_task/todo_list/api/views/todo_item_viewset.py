from typing import Dict, Any, List, Tuple

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
)

from todo_list.api.serializers.todo_item_serializer import (
    ToDoItemRetrieveSerializer, ToDoItemUpdateSerializer,
    ToDoItemCreateSerializer,
)
from todo_list.models import ToDoItem


class ToDoItemViewSet(viewsets.ModelViewSet):
    queryset = ToDoItem.objects.all()
    serializers = {
        'retrieve': ToDoItemRetrieveSerializer,
        'update': ToDoItemUpdateSerializer,
        'bulk_update': ToDoItemUpdateSerializer,
        'partial_update': ToDoItemUpdateSerializer,
        'create': ToDoItemCreateSerializer,
        'bulk_create': ToDoItemCreateSerializer,
        'default': ToDoItemRetrieveSerializer
    }
    filterset_fields = ['todo_list']

    def get_serializer_class(self) -> ModelSerializer:
        serializer_class = self.serializers.get(
            self.action,
            self.serializers.get('default'),
        )

        return serializer_class

    @action(
        methods=['POST'],
        detail=False,
    )
    def bulk_create(self, request: Request):
        """
        Use for mass items creation process
        """
        data = request.data
        if not isinstance(data, list):
            raise ValidationError('request data must be List instance')

        prepared_items, errors = self._parse_bulk_data(data)

        if any(errors):
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data=errors
            )

        resp_data = ToDoItem.objects.bulk_create(prepared_items)

        return Response(
            status=HTTP_201_CREATED,
            data=ToDoItemRetrieveSerializer(resp_data, many=True).data
        )

    @action(
        methods=['PUT'],
        detail=False,
    )
    def bulk_update(self, request: Request):
        """
        Use for mass items update process
        """
        data = request.data
        if not isinstance(data, list):
            raise ValidationError('request data must be List instance')

        prepared_items, errors = self._parse_bulk_data(data)

        if any(errors):
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data=errors
            )

        fields_to_update = set()
        for item in data:
            fields_to_update.update(item.keys())

        fields_to_update.remove('id')

        ToDoItem.objects.bulk_update(prepared_items, fields_to_update)

        return Response(
            status=HTTP_200_OK,
            data=data
        )

    def _parse_bulk_data(
        self,
        data: List[Dict[str, Any]]
    ) -> Tuple[List[ToDoItem], List[Dict[str, List[str]]]]:
        prepared_objects = []
        errors = []
        for item in data:
            ser = self.serializers.get(self.action)(data=item)
            try:
                if ser.is_valid(raise_exception=True):
                    prepared_objects.append(ToDoItem(**item))
                    errors.append({})
            except ValidationError as e:
                errors.append(e.detail)

        return prepared_objects, errors
