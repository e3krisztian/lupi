# coding: utf-8

# flake8: noqa

"""
    Lupi Game API

    # Least Unique Positive Integer (Lupi)  Lupi is a fun game, that has been studied a lot and has some maths behind how people behave and what really is optimal in some respect.  ## The Rules of the Game  - Lupi is a multiplayer game - each player picks a positive integer - the lowest unique integer wins   # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

__version__ = "1.0.0"

# import apis into sdk package
from lupi_game_client.api.game_api import GameApi
from lupi_game_client.api.stats_api import StatsApi

# import ApiClient
from lupi_game_client.api_client import ApiClient
from lupi_game_client.configuration import Configuration
from lupi_game_client.exceptions import OpenApiException
from lupi_game_client.exceptions import ApiTypeError
from lupi_game_client.exceptions import ApiValueError
from lupi_game_client.exceptions import ApiKeyError
from lupi_game_client.exceptions import ApiAttributeError
from lupi_game_client.exceptions import ApiException
# import models into sdk package
from lupi_game_client.models.list_of_rounds import ListOfRounds
from lupi_game_client.models.paging import Paging
from lupi_game_client.models.round import Round
from lupi_game_client.models.round_details import RoundDetails
from lupi_game_client.models.vote import Vote

