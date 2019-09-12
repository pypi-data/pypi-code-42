# coding: utf-8

"""
    Pure1 Public REST API

    Pure1 Public REST API, developed by [Pure Storage, Inc.](http://www.purestorage.com/)  [Knowledge base reference documentation](https://support.purestorage.com/Pure1/Pure1_Manage/Pure1_Manage_-_REST_API/Pure1_Manage_-_REST_API__Reference)  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from pypureclient.pure1.models.network_interface import NetworkInterface  # noqa: F401,E501
from pypureclient.pure1.models.page_info import PageInfo  # noqa: F401,E501


class NetworkInterfaceGetResponse(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'continuation_token': 'str',
        'total_item_count': 'int',
        'items': 'list[NetworkInterface]'
    }

    attribute_map = {
        'continuation_token': 'continuation_token',
        'total_item_count': 'total_item_count',
        'items': 'items'
    }

    def __init__(self, continuation_token=None, total_item_count=None, items=None):  # noqa: E501
        """NetworkInterfaceGetResponse - a model defined in Swagger"""  # noqa: E501

        self._continuation_token = None
        self._total_item_count = None
        self._items = None
        self.discriminator = None

        self.continuation_token = continuation_token
        self.total_item_count = total_item_count
        self.items = items

    @property
    def continuation_token(self):
        """Gets the continuation_token of this NetworkInterfaceGetResponse.  # noqa: E501

        Continuation token that can be provided in the continuation_token query param to get the next page of data. If you use the continuation token to page through data you are guaranteed to get all items exactly once regardless of how items are modified. If an item is added or deleted during the pagination then it may or may not be returned. The continuation token is generated if the limit is less than the remaining number of items, and the default sort is used (no sort is specified).  # noqa: E501

        :return: The continuation_token of this NetworkInterfaceGetResponse.  # noqa: E501
        :rtype: str
        """
        return self._continuation_token

    @continuation_token.setter
    def continuation_token(self, continuation_token):
        """Sets the continuation_token of this NetworkInterfaceGetResponse.

        Continuation token that can be provided in the continuation_token query param to get the next page of data. If you use the continuation token to page through data you are guaranteed to get all items exactly once regardless of how items are modified. If an item is added or deleted during the pagination then it may or may not be returned. The continuation token is generated if the limit is less than the remaining number of items, and the default sort is used (no sort is specified).  # noqa: E501

        :param continuation_token: The continuation_token of this NetworkInterfaceGetResponse.  # noqa: E501
        :type: str
        """

        self._continuation_token = continuation_token

    @property
    def total_item_count(self):
        """Gets the total_item_count of this NetworkInterfaceGetResponse.  # noqa: E501

        total number of items after applying filter params  # noqa: E501

        :return: The total_item_count of this NetworkInterfaceGetResponse.  # noqa: E501
        :rtype: int
        """
        return self._total_item_count

    @total_item_count.setter
    def total_item_count(self, total_item_count):
        """Sets the total_item_count of this NetworkInterfaceGetResponse.

        total number of items after applying filter params  # noqa: E501

        :param total_item_count: The total_item_count of this NetworkInterfaceGetResponse.  # noqa: E501
        :type: int
        """

        self._total_item_count = total_item_count

    @property
    def items(self):
        """Gets the items of this NetworkInterfaceGetResponse.  # noqa: E501

        a list of network interface objects  # noqa: E501

        :return: The items of this NetworkInterfaceGetResponse.  # noqa: E501
        :rtype: list[NetworkInterface]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this NetworkInterfaceGetResponse.

        a list of network interface objects  # noqa: E501

        :param items: The items of this NetworkInterfaceGetResponse.  # noqa: E501
        :type: list[NetworkInterface]
        """

        self._items = items

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(NetworkInterfaceGetResponse, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, NetworkInterfaceGetResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
