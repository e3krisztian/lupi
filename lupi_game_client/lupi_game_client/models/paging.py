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


class Paging(object):
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
        'before': 'int',
        'page_size': 'int'
    }

    attribute_map = {
        'before': 'before',
        'page_size': 'page_size'
    }

    def __init__(self, before=None, page_size=25, local_vars_configuration=None):  # noqa: E501
        """Paging - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._before = None
        self._page_size = None
        self.discriminator = None

        self.before = before
        self.page_size = page_size

    @property
    def before(self):
        """Gets the before of this Paging.  # noqa: E501


        :return: The before of this Paging.  # noqa: E501
        :rtype: int
        """
        return self._before

    @before.setter
    def before(self, before):
        """Sets the before of this Paging.


        :param before: The before of this Paging.  # noqa: E501
        :type before: int
        """
        if self.local_vars_configuration.client_side_validation and before is None:  # noqa: E501
            raise ValueError("Invalid value for `before`, must not be `None`")  # noqa: E501

        self._before = before

    @property
    def page_size(self):
        """Gets the page_size of this Paging.  # noqa: E501


        :return: The page_size of this Paging.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this Paging.


        :param page_size: The page_size of this Paging.  # noqa: E501
        :type page_size: int
        """
        if self.local_vars_configuration.client_side_validation and page_size is None:  # noqa: E501
            raise ValueError("Invalid value for `page_size`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                page_size is not None and page_size > 100):  # noqa: E501
            raise ValueError("Invalid value for `page_size`, must be a value less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                page_size is not None and page_size < 1):  # noqa: E501
            raise ValueError("Invalid value for `page_size`, must be a value greater than or equal to `1`")  # noqa: E501

        self._page_size = page_size

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
        if not isinstance(other, Paging):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Paging):
            return True

        return self.to_dict() != other.to_dict()
