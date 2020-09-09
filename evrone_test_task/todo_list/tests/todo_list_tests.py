import pytest
from rest_framework.test import APIClient
from django.conf import settings

from todo_list.models import ToDoList


@pytest.mark.django_db
def test_retrieve_lists_many():
    client = APIClient()
    limit = settings.REST_FRAMEWORK['PAGE_SIZE']
    all_lists_count = ToDoList.objects.all().count()
    resp = client.get('/api/v1/todo_list/')

    assert resp.status_code == 200
    assert resp.data['next'] == (
        f'http://testserver/api/v1/todo_list/?limit={limit}&offset={limit}'
    )
    assert not resp.data['previous']
    assert resp.data['count'] == all_lists_count


@pytest.mark.django_db
def test_retrieve_lists_detail():
    client = APIClient()
    todo_list_data = {'title': 'test_title'}
    todo_list = ToDoList.objects.create(**todo_list_data)
    resp = client.get(f'/api/v1/todo_list/{todo_list.id}/')

    assert resp.status_code == 200
    assert resp.data['id'] == todo_list.id
    assert resp.data['title'] == todo_list.title


@pytest.mark.django_db
def test_post_todo_list():
    client = APIClient()
    todo_list_data = {
        'title': 'test_title'
    }

    resp = client.post('/api/v1/todo_list/', todo_list_data, format='json')

    assert resp.status_code == 201
    assert resp.data['title'] == 'test_title'


@pytest.mark.django_db
def test_update_todo_list():
    client = APIClient()
    initial_todo_list_data = {'title': 'test_title'}
    todo_list = ToDoList.objects.create(**initial_todo_list_data)
    updated_todo_list_data = {
        'title': 'updated_title',
        'id': todo_list.id
    }

    resp = client.put(
        f'/api/v1/todo_list/{todo_list.id}/',
        updated_todo_list_data,
    )

    assert resp.status_code == 200
    assert resp.data['title'] == updated_todo_list_data['title']


@pytest.mark.django_db
def test_delete_todo_list():
    client = APIClient()
    todo_list_data = {'title': 'test_title'}
    todo_list = ToDoList.objects.create(**todo_list_data)
    resp = client.delete(f'/api/v1/todo_list/{todo_list.id}/')

    assert resp.status_code == 204

    resp = client.get(f'/api/v1/todo_list/{todo_list.id}/')

    assert resp.status_code == 404


@pytest.mark.django_db
def test_create_todo_list_empty_title():
    client = APIClient()
    todo_list_data = {
        'title': ''
    }

    resp = client.post('/api/v1/todo_list/', todo_list_data, format='json')

    assert resp.status_code == 400


@pytest.mark.parametrize(
    'items, search_string, found_count',
    [
        ([{'title': 'parol` tetriandoh'}, {'title': 'tetriandoh'}], 'parol` tetriandoh', 1),
        ([{'title': 'parol` tetriandoh'}, {'title': 'tetriandoh parol`'}], 'tetriandoh', 2),
        ([{'title': 'parol` tetriandoh'}, {'title': 'another title'}], 'qwerty', 0),
    ]
)
@pytest.mark.django_db
def test_search_todo_list(items, search_string, found_count):
    client = APIClient()
    for attrs in items:
        ToDoList.objects.create(**attrs)

    resp = client.get(f'/api/v1/todo_list/?search={search_string}')

    assert resp.status_code == 200
    assert len(resp.data['results']) == found_count
