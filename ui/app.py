import flask
from flask.templating import render_template

ui = flask.Blueprint('lupi ui', __name__)


@ui.route('/')
def index():
    return render_template('main_page.html')


def create_app(testing=False):
    app = flask.Flask(__name__)
    app.register_blueprint(ui)
    app.config['TESTING'] = testing
    return app


if __name__ == '__main__':
    app = create_app(testing=True)
    app.run(host='127.0.0.1', port='5000', debug=True)
