# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class RequestValidator(pulumi.CustomResource):
    name: pulumi.Output[str]
    """
    The name of the request validator
    """
    rest_api: pulumi.Output[str]
    """
    The ID of the associated Rest API
    """
    validate_request_body: pulumi.Output[bool]
    """
    Boolean whether to validate request body. Defaults to `false`.
    """
    validate_request_parameters: pulumi.Output[bool]
    """
    Boolean whether to validate request parameters. Defaults to `false`.
    """
    def __init__(__self__, resource_name, opts=None, name=None, rest_api=None, validate_request_body=None, validate_request_parameters=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an API Gateway Request Validator.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the request validator
        :param pulumi.Input[str] rest_api: The ID of the associated Rest API
        :param pulumi.Input[bool] validate_request_body: Boolean whether to validate request body. Defaults to `false`.
        :param pulumi.Input[bool] validate_request_parameters: Boolean whether to validate request parameters. Defaults to `false`.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/api_gateway_request_validator.html.markdown.
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

            __props__['name'] = name
            if rest_api is None:
                raise TypeError("Missing required property 'rest_api'")
            __props__['rest_api'] = rest_api
            __props__['validate_request_body'] = validate_request_body
            __props__['validate_request_parameters'] = validate_request_parameters
        super(RequestValidator, __self__).__init__(
            'aws:apigateway/requestValidator:RequestValidator',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, name=None, rest_api=None, validate_request_body=None, validate_request_parameters=None):
        """
        Get an existing RequestValidator resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the request validator
        :param pulumi.Input[str] rest_api: The ID of the associated Rest API
        :param pulumi.Input[bool] validate_request_body: Boolean whether to validate request body. Defaults to `false`.
        :param pulumi.Input[bool] validate_request_parameters: Boolean whether to validate request parameters. Defaults to `false`.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/api_gateway_request_validator.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["name"] = name
        __props__["rest_api"] = rest_api
        __props__["validate_request_body"] = validate_request_body
        __props__["validate_request_parameters"] = validate_request_parameters
        return RequestValidator(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

