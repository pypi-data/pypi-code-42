# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from ....properties import Property
import pprint
import re

import six


class ResourcePerformanceGetResponse(object):


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'more_items_remaining': 'bool',
        'total_item_count': 'int',
        'items': 'list[ResourcePerformance]',
        'total': 'list[ResourcePerformance]'
    }

    attribute_map = {
        'more_items_remaining': 'more_items_remaining',
        'total_item_count': 'total_item_count',
        'items': 'items',
        'total': 'total'
    }

    required_args = {
    }

    def __init__(self, **kwargs):
        """
        Keyword args:
            more_items_remaining (bool): Returns a value of `true` if subsequent items can be retrieved.
            total_item_count (int): The total number of records after applying all filter query parameters. The `total_item_count` will be calculated if and only if the corresponding query parameter `total_item_count` is set to `true`. If this query parameter is not set or set to `false`, a value of `null` will be returned.
            items (list[ResourcePerformance]): Performance data. If `total_only=true`, the `items` list will be empty.
            total (list[ResourcePerformance]): The aggregate value of all items after filtering. Where it makes more sense, the average value is displayed instead. The values are displayed for each field where meaningful.
        """
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])
        for arg in self.required_args:
            if arg not in kwargs:
                raise Exception("Required argument {} is missing".format(arg))

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `ResourcePerformanceGetResponse`".format(key))
        self.__dict__[key] = value

    def __getattribute__(self, item):
        value = object.__getattribute__(self, item)
        if isinstance(value, Property):
            raise AttributeError
        else:
            return value

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            if hasattr(self, attr):
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
        if issubclass(ResourcePerformanceGetResponse, dict):
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
        if not isinstance(other, ResourcePerformanceGetResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
