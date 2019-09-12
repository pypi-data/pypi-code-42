# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class ReceiptFilter(pulumi.CustomResource):
    cidr: pulumi.Output[str]
    """
    The IP address or address range to filter, in CIDR notation
    """
    name: pulumi.Output[str]
    """
    The name of the filter
    """
    policy: pulumi.Output[str]
    """
    Block or Allow
    """
    def __init__(__self__, resource_name, opts=None, cidr=None, name=None, policy=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an SES receipt filter resource
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cidr: The IP address or address range to filter, in CIDR notation
        :param pulumi.Input[str] name: The name of the filter
        :param pulumi.Input[str] policy: Block or Allow

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/ses_receipt_filter.html.markdown.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            if cidr is None:
                raise TypeError("Missing required property 'cidr'")
            __props__['cidr'] = cidr
            __props__['name'] = name
            if policy is None:
                raise TypeError("Missing required property 'policy'")
            __props__['policy'] = policy
        super(ReceiptFilter, __self__).__init__(
            'aws:ses/receiptFilter:ReceiptFilter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, cidr=None, name=None, policy=None):
        """
        Get an existing ReceiptFilter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cidr: The IP address or address range to filter, in CIDR notation
        :param pulumi.Input[str] name: The name of the filter
        :param pulumi.Input[str] policy: Block or Allow

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/ses_receipt_filter.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["cidr"] = cidr
        __props__["name"] = name
        __props__["policy"] = policy
        return ReceiptFilter(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

