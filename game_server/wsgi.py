import os
from .app import create_app

app = create_app(os.environ['LUPI_DB_URI'])
