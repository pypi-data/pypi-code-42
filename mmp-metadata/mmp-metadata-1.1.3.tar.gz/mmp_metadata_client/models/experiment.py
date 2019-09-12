# coding: utf-8

"""
    MMP Metadata

    This is a API for MMP Metadata  # noqa: E501

    The version of the OpenAPI document: 1.0.0-oas3
    Contact: st116848@stud.uni-stuttgart.de.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class Experiment(object):
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
        'id': 'str',
        'name': 'str',
        'version': 'str',
        'create_time': 'datetime',
        'runs': 'list[Run]',
        'annotations': 'dict(str, str)'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'version': 'version',
        'create_time': 'createTime',
        'runs': 'runs',
        'annotations': 'annotations'
    }

    def __init__(self, id=None, name=None, version=None, create_time=None, runs=None, annotations=None):  # noqa: E501
        """Experiment - a model defined in OpenAPI"""  # noqa: E501

        self._id = None
        self._name = None
        self._version = None
        self._create_time = None
        self._runs = None
        self._annotations = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.name = name
        self.version = version
        if create_time is not None:
            self.create_time = create_time
        if runs is not None:
            self.runs = runs
        if annotations is not None:
            self.annotations = annotations

    @property
    def id(self):
        """Gets the id of this Experiment.  # noqa: E501


        :return: The id of this Experiment.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Experiment.


        :param id: The id of this Experiment.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Experiment.  # noqa: E501


        :return: The name of this Experiment.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Experiment.


        :param name: The name of this Experiment.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def version(self):
        """Gets the version of this Experiment.  # noqa: E501


        :return: The version of this Experiment.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Experiment.


        :param version: The version of this Experiment.  # noqa: E501
        :type: str
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def create_time(self):
        """Gets the create_time of this Experiment.  # noqa: E501


        :return: The create_time of this Experiment.  # noqa: E501
        :rtype: datetime
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this Experiment.


        :param create_time: The create_time of this Experiment.  # noqa: E501
        :type: datetime
        """

        self._create_time = create_time

    @property
    def runs(self):
        """Gets the runs of this Experiment.  # noqa: E501


        :return: The runs of this Experiment.  # noqa: E501
        :rtype: list[Run]
        """
        return self._runs

    @runs.setter
    def runs(self, runs):
        """Sets the runs of this Experiment.


        :param runs: The runs of this Experiment.  # noqa: E501
        :type: list[Run]
        """

        self._runs = runs

    @property
    def annotations(self):
        """Gets the annotations of this Experiment.  # noqa: E501


        :return: The annotations of this Experiment.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._annotations

    @annotations.setter
    def annotations(self, annotations):
        """Sets the annotations of this Experiment.


        :param annotations: The annotations of this Experiment.  # noqa: E501
        :type: dict(str, str)
        """

        self._annotations = annotations

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
        if not isinstance(other, Experiment):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
