from . import model

import connexion
from connexion.resolver import RestyResolver


def create_app(db_uri, testing=False):
    connexion_app = connexion.FlaskApp(
        __name__,
        # specification_dir=openapi_path,
        # options={"swagger_ui": False, "serve_spec": False},
    )
    connexion_app.add_api("../openapi.yaml", strict_validation=True, validate_responses=True)
    flask_app = connexion_app.app
    # flask_app.json_encoder = encoder.JSONEncoder

    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['TESTING'] = True
    model.db.init_app(flask_app)
    return flask_app


def create_db(app):
    with app.app_context():
        model.db.create_all()


if __name__ == '__main__':
    # TODO: remove test code
    app = create_app('sqlite:///x.sqlite')
    create_db(app)
    app = create_app('sqlite:///:memory:')
    create_db(app)
    app.run(host='127.0.0.1', port='5000', debug=True)
