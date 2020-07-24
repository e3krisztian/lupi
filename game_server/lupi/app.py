from . import model

import connexion
from connexion.resolver import RestyResolver


def create_app(db_uri):
    connexion_app = connexion.FlaskApp(
        __name__,
        # specification_dir=openapi_path,
        # options={"swagger_ui": False, "serve_spec": False},
    )
    connexion_app.add_api("../openapi.yaml", strict_validation=True, resolver=RestyResolver("lupi.api"))
    flask_app = connexion_app.app
    # flask_app.json_encoder = encoder.JSONEncoder

    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    model.db.init_app(flask_app)
    return flask_app


def create_db(app):
    with app.app_context():
        model.db.create_all()


# TODO: test code
app = create_app('sqlite:///x.sqlite')
create_db(app)
create_app('sqlite:///:memory:')
