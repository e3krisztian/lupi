from .app import create_app
from . import model

import connexion
import pytest

@pytest.fixture(scope="session")
def _app():
    app = create_app('sqlite:///:memory:', testing=True)
    return app


@pytest.fixture
def db(_app):
    """
    Enable Flask-SQLAlchemy to have access to a SQLAlchemy session
    """
    with _app.app_context():
        model.db.drop_all()
        model.db.create_all()
        yield model.db
        model.db.drop_all()

@pytest.fixture
def client(db, _app):
    with _app.test_client() as client:
        yield client

