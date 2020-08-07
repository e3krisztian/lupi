# Lupi

Least Unique Positive Integer is a fun game and now that people are stuck in home office it can be a great way to have to start the day with a common activity. The game has been studied a lot and has some maths behind how people behave and what really is optimal in some respect.


## Game Rules

It is a Multiplayer game, each player picks a positive integer. The lowest unique integer wins.


## Implementation

Focus is on the API that enables this game service and only provide a very basic GUI.


## Components

- `db` (PostgreSQL)
- `lupi_game_server`
- `lupi_ui`

There is also another top level directory: `lupi_game_client`, which is a generated client library for `lupi_game_server`, used by `lupi_ui`.

`lupi_game_server` and `lupi_ui` are stateless servers, they can be restarted at will.


### Source

The source layout is flat, tests and other non-python files are mixed inside the project directories - because there are not many of them.

Main starting points for looking into the source:


#### [`Makefile`](Makefile)

Command center, see below for what it can be used for.


#### `lupi_game_server`

- [`openapi.yaml`](lupi_game_server/openapi.yaml) is the [OpenAPI](https://swagger.io/specification/) description of the RESTful API for the game (also source of the generated `lupi_game_client`)
- [`api.py`](lupi_game_server/api.py) implements the REST API defined in the above `yaml` file
- [`model.py`](lupi_game_server/model.py) is the very simple database model
- [`game.py`](lupi_game_server/game.py) and [`stats.py`](lupi_game_server/stats.py) implements the `db` access and game logic

`lupi_game_server` uses `connexion[swagger-ui]`, it gives a working UI and documentation for the live API (documentation/structure can also be viewed by pasting the `openapi.yaml` file to https://editor.swagger.io/).

`make info` or `docker-compose run info` gives an URL for the swagger UI (`game_server API:   http://192.168.16.3:8080/v1/ui`):
```
$  docker-compose run --rm info
Starting lupi_db_1 ... done
Starting lupi_game_server_1 ... done
Starting lupi_ui_1          ... done
IP addresses of containers:
  db:          192.168.16.2
  game_server: 192.168.16.3
  ui:          192.168.16.4

Accessible internal services of interest:
  game_server API:   http://192.168.16.3:8080/v1/ui
  ui (in container): http://192.168.16.4:8080
```


#### `lupi_ui`

Is a simple Flask application with templates. It uses the `lupi_game_server` via [`game_server`](lupi_ui/game_server.py) which is a minimal wrapper around `lupi_game_client`

WARNING: it is only halfway done with TDD (time constraint), so there are untested bits.

The tests of this component is more like an integration test - the entire system is started.


## Development infrastructure

- runtime: [Python 3.8](https://www.python.org/)
- dependency management: [Poetry](https://python-poetry.org/)
- runtime & test environment: [docker-compose](https://docs.docker.com/compose/)
- automation: [GNU make](https://www.gnu.org/software/make/manual/make.html)
- text editor: [VS Code](https://code.visualstudio.com/)
- code generation: [OpenAPI Generator](https://openapi-generator.tech/docs/installation/#docker)
- database: [PostgreSQL](https://www.postgresql.org/)


## Python libs

- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Flask-Table
- connexion[swagger-ui]


## Building the containers

```bash
make build
```
which is equivalent with
```bash
docker-compose build
```
on a clean workspace, but triggers code generation when certain files change.


## Running the system

```bash
docker-compose up
```

Port `8080` will be mapped to the web ui (http://localhost:8080).

NOTE, that there is no production configuration (it is a toy), the database is stored in RAM (tmpfs), so all data is lost when the db server is stopped (e.g. tests restart the `db` to start from an empty database).


## Initializing the database

The schema is created by a tool, that is started with `docker-compose up` and also with `make test`.

In case the schema is not created, it can be triggered with `make initdb`

There is no need to stop the services - they are stateless.


## Running the tests

```bash
make build
make
```

Running the tests (75 in total) takes ~13sec on a 10y old notebook.


## Peeking into containers

e.g. `db` container - psql console:

```bash
make shell/db
```

There is also `shell/ui` and `shell/game_server`.
