from .app import create_app

import pytest

@pytest.fixture
def client():
    with create_app(testing=True).test_client() as client:
        yield client
