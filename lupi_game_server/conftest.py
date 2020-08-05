from .app import create_app
from . import model

import connexion
import pytest

@pytest.fixture(scope="session")
def flask_app():
    app = create_app('sqlite:///:memory:', testing=True)
    return app


@pytest.fixture
def db(flask_app):
    """
    Enable Flask-SQLAlchemy to have access to a SQLAlchemy session
    """
    with flask_app.app_context():
        model.db.drop_all()
        model.db.create_all()
        yield model.db
        model.db.drop_all()

@pytest.fixture
def client(db, flask_app):
    with flask_app.test_client() as client:
        yield client

