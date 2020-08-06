"""
Wrapper around generated package lupi_game_client

Usage:
>>> from lupi_ui import game_server
>>> # ...
>>> with game_server.open() as server:
...     round_id = server.game.create_round()
...     ...

"""
import contextlib
from dataclasses import dataclass

import lupi_game_client

ApiException = lupi_game_client.ApiException


v1_configuration = lupi_game_client.Configuration(
    host = "http://game_server:8080/v1"
)


@dataclass
class ServerApi:
    game: lupi_game_client.GameApi
    stats: lupi_game_client.StatsApi


@contextlib.contextmanager
def open() -> ServerApi:
    with lupi_game_client.ApiClient(v1_configuration) as api_client:
        yield ServerApi(
            lupi_game_client.GameApi(api_client),
            lupi_game_client.StatsApi(api_client)
        )
