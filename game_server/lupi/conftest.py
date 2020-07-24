from .app import create_app
from . import model

import connexion
import pytest

@pytest.fixture(scope="session")
def app():
    app = create_app('sqlite:///:memory:')
    return app


@pytest.fixture
def db(app):
    """
    Enable Flask-SQLAlchemy to have access to a SQLAlchemy session
    """
    with app.app_context():
        yield model.db
