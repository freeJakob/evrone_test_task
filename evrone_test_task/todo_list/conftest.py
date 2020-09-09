import pytest

from todo_list.test_factories.todo_list_factories import ToDoListFactory


@pytest.fixture(autouse=True)
def populate_test_db():
    ToDoListFactory.create_batch(15)
