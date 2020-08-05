# coding: utf-8

"""
    Lupi Game API

    # Least Unique Positive Integer (Lupi)  Lupi is a fun game, that has been studied a lot and has some maths behind how people behave and what really is optimal in some respect.  ## The Rules of the Game  - Lupi is a multiplayer game - each player picks a positive integer - the lowest unique integer wins   # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import lupi_game_client
from lupi_game_client.api.stats_api import StatsApi  # noqa: E501
from lupi_game_client.rest import ApiException


class TestStatsApi(unittest.TestCase):
    """StatsApi unit test stubs"""

    def setUp(self):
        self.api = lupi_game_client.api.stats_api.StatsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_round(self):
        """Test case for get_round

        """
        pass

    def test_get_round_result(self):
        """Test case for get_round_result

        """
        pass

    def test_get_rounds(self):
        """Test case for get_rounds

        """
        pass


if __name__ == '__main__':
    unittest.main()