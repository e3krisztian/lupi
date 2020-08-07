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
from lupi_game_client.api.game_api import GameApi  # noqa: E501
from lupi_game_client.rest import ApiException


class TestGameApi(unittest.TestCase):
    """GameApi unit test stubs"""

    def setUp(self):
        self.api = lupi_game_client.api.game_api.GameApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_vote(self):
        """Test case for add_vote

        """
        pass

    def test_create_round(self):
        """Test case for create_round

        """
        pass

    def test_get_current_round_id(self):
        """Test case for get_current_round_id

        """
        pass

    def test_get_round(self):
        """Test case for get_round

        """
        pass

    def test_set_round_completed(self):
        """Test case for set_round_completed

        """
        pass


if __name__ == '__main__':
    unittest.main()
