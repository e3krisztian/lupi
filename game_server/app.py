from . import model

import connexion


def create_app(db_uri, testing=False):
    connexion_app = connexion.FlaskApp(
        __name__,
        # options={"swagger_ui": False, "serve_spec": False},
    )
    connexion_app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)
    flask_app = connexion_app.app

    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['TESTING'] = testing
    # print(flask_app.config)
    model.db.init_app(flask_app)
    return flask_app


if __name__ == '__main__':
    import os
    app = create_app(os.environ['LUPI_DB_URI'])
    app.run(host='127.0.0.1', port='5000', debug=False)
