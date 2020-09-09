import pytest
from django.conf import settings
from rest_framework.test import APIClient

from todo_list.models import ToDoItem, ToDoList


@pytest.mark.django_db
def test_retrieve_lists_many():
    client = APIClient()
    limit = settings.REST_FRAMEWORK['PAGE_SIZE']
    all_items_count = ToDoList.objects.all().count()
    resp = client.get('/api/v1/todo_item/')

    assert resp.status_code == 200
    assert resp.data['next'] == (
        f'http://testserver/api/v1/todo_item/?limit={limit}&offset={limit}'
    )
    assert not resp.data['previous']
    assert resp.data['count'] == all_items_count


@pytest.mark.django_db
def test_retrieve_item_detail():
    client = APIClient()
    todo_list_data = {'title': 'test_title'}
    todo_list = ToDoList.objects.create(**todo_list_data)
    todo_item_data = {'title': 'test_title', 'todo_list_id': todo_list.id}
    todo_item = ToDoItem.objects.create(**todo_item_data)
    resp = client.get(f'/api/v1/todo_item/{todo_item.id}/')

    assert resp.status_code == 200
    assert resp.data['id'] == todo_item.id
    assert resp.data['title'] == todo_item.title


@pytest.mark.django_db
def test_retrieve_items_by_list_id():
    client = APIClient()
    todo_list_data = {'title': 'test_title'}
    todo_list = ToDoList.objects.create(**todo_list_data)
    todo_item_data = {'title': 'test_title', 'todo_list_id': todo_list.id}
    ToDoItem.objects.create(**todo_item_data)
    ToDoItem.objects.create(**todo_item_data)

    resp = client.get(
        f'/api/v1/todo_item/?todo_list={todo_list.id}'
    )

    assert resp.status_code == 200
    assert resp.data['count'] == 2


@pytest.mark.django_db
def test_post_todo_item():
    client = APIClient()
    todo_list_data = {'title': 'test_title'}
    todo_list = ToDoList.objects.create(**todo_list_data)
    todo_item_data = {'title': 'test_title', 'todo_list_id': todo_list.id}

    resp = client.post('/api/v1/todo_item/', todo_item_data, format='json')

    assert resp.status_code == 201
    assert resp.data['title'] == 'test_title'


@pytest.mark.django_db
def test_update_todo_item():
    client = APIClient()
    todo_list_data = {'title': 'test_title'}
    todo_list = ToDoList.objects.create(**todo_list_data)
    todo_item_data = {'title': 'test_title', 'todo_list_id': todo_list.id}
    todo_item = ToDoItem.objects.create(**todo_item_data)
    updated_todo_item_data = {
        'title': 'updated_title',
        'id': todo_item.id
    }

    resp = client.put(
        f'/api/v1/todo_item/{todo_item.id}/',
        updated_todo_item_data,
    )

    assert resp.status_code == 200
    assert resp.data['title'] == updated_todo_item_data['title']


@pytest.mark.django_db
def test_delete_todo_item():
    client = APIClient()
    todo_list_data = {'title': 'test_title'}
    todo_list = ToDoList.objects.create(**todo_list_data)
    todo_item_data = {'title': 'test_title', 'todo_list_id': todo_list.id}
    todo_item = ToDoItem.objects.create(**todo_item_data)
    resp = client.delete(f'/api/v1/todo_item/{todo_item.id}/')

    assert resp.status_code == 204

    resp = client.get(f'/api/v1/todo_item/{todo_item.id}/')

    assert resp.status_code == 404


@pytest.mark.django_db
def test_bulk_create_todo_items():
    client = APIClient()
    todo_list_data = {'title': 'test_title'}
    todo_list = ToDoList.objects.create(**todo_list_data)
    items_bulk_data = [
        {'title': 'test_title', 'todo_list_id': todo_list.id},
        {'title': 'test_title_2', 'todo_list_id': todo_list.id}
    ]

    resp = client.post(
        f'/api/v1/todo_item/bulk_create/',
        items_bulk_data,
        format='json',
    )

    assert resp.status_code == 201
    assert len(resp.data) == 2


@pytest.mark.django_db
def test_bulk_update_todo_items():
    client = APIClient()
    todo_list_data = {'title': 'test_title'}
    todo_list = ToDoList.objects.create(**todo_list_data)
    item1 = ToDoItem.objects.create(
        title='test_title',
        todo_list_id=todo_list.id
    )
    item2 = ToDoItem.objects.create(
        title='test_title_2',
        todo_list_id=todo_list.id
    )
    updated_items_bulk_data = [
        {'title': 'updated_title', 'id': item1.id},
        {'title': 'updated_title_2', 'id': item2.id}
    ]

    resp = client.put(
        f'/api/v1/todo_item/bulk_update/',
        updated_items_bulk_data,
        format='json',
    )

    assert resp.status_code == 200
    assert len(resp.data) == 2
    assert resp.data[0]['title'] == 'updated_title'
    assert resp.data[1]['title'] == 'updated_title_2'
