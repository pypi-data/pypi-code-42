# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class GetRegionResult:
    """
    A collection of values returned by getRegion.
    """
    def __init__(__self__, description=None, endpoint=None, name=None, id=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        __self__.description = description
        """
        The region's description in this format: "Location (Region name)".
        """
        if endpoint and not isinstance(endpoint, str):
            raise TypeError("Expected argument 'endpoint' to be a str")
        __self__.endpoint = endpoint
        """
        The EC2 endpoint for the selected region.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        """
        The name of the selected region.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
class AwaitableGetRegionResult(GetRegionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRegionResult(
            description=self.description,
            endpoint=self.endpoint,
            name=self.name,
            id=self.id)

def get_region(endpoint=None,name=None,opts=None):
    """
    `.getRegion` provides details about a specific AWS region.
    
    As well as validating a given region name this resource can be used to
    discover the name of the region configured within the provider. The latter
    can be useful in a child module which is inheriting an AWS provider
    configuration from its parent module.
    
    :param str endpoint: The EC2 endpoint of the region to select.
    :param str name: The full name of the region to select.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/d/region.html.markdown.
    """
    __args__ = dict()

    __args__['endpoint'] = endpoint
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:index/getRegion:getRegion', __args__, opts=opts).value

    return AwaitableGetRegionResult(
        description=__ret__.get('description'),
        endpoint=__ret__.get('endpoint'),
        name=__ret__.get('name'),
        id=__ret__.get('id'))
