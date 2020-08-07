# coding: utf-8

"""
    Lupi Game API

    # Least Unique Positive Integer (Lupi)  Lupi is a fun game, that has been studied a lot and has some maths behind how people behave and what really is optimal in some respect.  ## The Rules of the Game  - Lupi is a multiplayer game - each player picks a positive integer - the lowest unique integer wins   # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from lupi_game_client.configuration import Configuration


class RoundDetails(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'id': 'int',
        'start_date': 'datetime',
        'end_date': 'datetime',
        'players': 'int',
        'is_completed': 'bool',
        'winner': 'str',
        'vote': 'int'
    }

    attribute_map = {
        'id': 'id',
        'start_date': 'start_date',
        'end_date': 'end_date',
        'players': 'players',
        'is_completed': 'is_completed',
        'winner': 'winner',
        'vote': 'vote'
    }

    def __init__(self, id=None, start_date=None, end_date=None, players=None, is_completed=None, winner=None, vote=None, local_vars_configuration=None):  # noqa: E501
        """RoundDetails - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._start_date = None
        self._end_date = None
        self._players = None
        self._is_completed = None
        self._winner = None
        self._vote = None
        self.discriminator = None

        self.id = id
        self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date
        if players is not None:
            self.players = players
        self.is_completed = is_completed
        if winner is not None:
            self.winner = winner
        if vote is not None:
            self.vote = vote

    @property
    def id(self):
        """Gets the id of this RoundDetails.  # noqa: E501


        :return: The id of this RoundDetails.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this RoundDetails.


        :param id: The id of this RoundDetails.  # noqa: E501
        :type id: int
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def start_date(self):
        """Gets the start_date of this RoundDetails.  # noqa: E501


        :return: The start_date of this RoundDetails.  # noqa: E501
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this RoundDetails.


        :param start_date: The start_date of this RoundDetails.  # noqa: E501
        :type start_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and start_date is None:  # noqa: E501
            raise ValueError("Invalid value for `start_date`, must not be `None`")  # noqa: E501

        self._start_date = start_date

    @property
    def end_date(self):
        """Gets the end_date of this RoundDetails.  # noqa: E501


        :return: The end_date of this RoundDetails.  # noqa: E501
        :rtype: datetime
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """Sets the end_date of this RoundDetails.


        :param end_date: The end_date of this RoundDetails.  # noqa: E501
        :type end_date: datetime
        """

        self._end_date = end_date

    @property
    def players(self):
        """Gets the players of this RoundDetails.  # noqa: E501


        :return: The players of this RoundDetails.  # noqa: E501
        :rtype: int
        """
        return self._players

    @players.setter
    def players(self, players):
        """Sets the players of this RoundDetails.


        :param players: The players of this RoundDetails.  # noqa: E501
        :type players: int
        """
        if (self.local_vars_configuration.client_side_validation and
                players is not None and players < 0):  # noqa: E501
            raise ValueError("Invalid value for `players`, must be a value greater than or equal to `0`")  # noqa: E501

        self._players = players

    @property
    def is_completed(self):
        """Gets the is_completed of this RoundDetails.  # noqa: E501


        :return: The is_completed of this RoundDetails.  # noqa: E501
        :rtype: bool
        """
        return self._is_completed

    @is_completed.setter
    def is_completed(self, is_completed):
        """Sets the is_completed of this RoundDetails.


        :param is_completed: The is_completed of this RoundDetails.  # noqa: E501
        :type is_completed: bool
        """
        if self.local_vars_configuration.client_side_validation and is_completed is None:  # noqa: E501
            raise ValueError("Invalid value for `is_completed`, must not be `None`")  # noqa: E501

        self._is_completed = is_completed

    @property
    def winner(self):
        """Gets the winner of this RoundDetails.  # noqa: E501


        :return: The winner of this RoundDetails.  # noqa: E501
        :rtype: str
        """
        return self._winner

    @winner.setter
    def winner(self, winner):
        """Sets the winner of this RoundDetails.


        :param winner: The winner of this RoundDetails.  # noqa: E501
        :type winner: str
        """

        self._winner = winner

    @property
    def vote(self):
        """Gets the vote of this RoundDetails.  # noqa: E501


        :return: The vote of this RoundDetails.  # noqa: E501
        :rtype: int
        """
        return self._vote

    @vote.setter
    def vote(self, vote):
        """Sets the vote of this RoundDetails.


        :param vote: The vote of this RoundDetails.  # noqa: E501
        :type vote: int
        """
        if (self.local_vars_configuration.client_side_validation and
                vote is not None and vote < 1):  # noqa: E501
            raise ValueError("Invalid value for `vote`, must be a value greater than or equal to `1`")  # noqa: E501

        self._vote = vote

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RoundDetails):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RoundDetails):
            return True

        return self.to_dict() != other.to_dict()
