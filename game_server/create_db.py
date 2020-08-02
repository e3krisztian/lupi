import os
from . import model
from . app import create_app


def main():
    app = create_app(os.environ['LUPI_DB_URI'])
    with app.app_context():
        model.db.create_all()


if __name__ == '__main__':
    main()
