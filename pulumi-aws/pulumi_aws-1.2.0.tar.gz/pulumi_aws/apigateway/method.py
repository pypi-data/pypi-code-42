# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Method(pulumi.CustomResource):
    api_key_required: pulumi.Output[bool]
    """
    Specify if the method requires an API key
    """
    authorization: pulumi.Output[str]
    """
    The type of authorization used for the method (`NONE`, `CUSTOM`, `AWS_IAM`, `COGNITO_USER_POOLS`)
    """
    authorization_scopes: pulumi.Output[list]
    """
    The authorization scopes used when the authorization is `COGNITO_USER_POOLS`
    """
    authorizer_id: pulumi.Output[str]
    """
    The authorizer id to be used when the authorization is `CUSTOM` or `COGNITO_USER_POOLS`
    """
    http_method: pulumi.Output[str]
    """
    The HTTP Method (`GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `OPTIONS`, `ANY`)
    """
    request_models: pulumi.Output[dict]
    """
    A map of the API models used for the request's content type
    where key is the content type (e.g. `application/json`)
    and value is either `Error`, `Empty` (built-in models) or `apigateway.Model`'s `name`.
    """
    request_parameters: pulumi.Output[dict]
    """
    A map of request query string parameters and headers that should be passed to the integration.
    For example: `request_parameters = {"method.request.header.X-Some-Header" = true "method.request.querystring.some-query-param" = true}` would define that the header `X-Some-Header` and the query string `some-query-param` must be provided in the request
    """
    request_validator_id: pulumi.Output[str]
    """
    The ID of a `apigateway.RequestValidator`
    """
    resource_id: pulumi.Output[str]
    """
    The API resource ID
    """
    rest_api: pulumi.Output[str]
    """
    The ID of the associated REST API
    """
    def __init__(__self__, resource_name, opts=None, api_key_required=None, authorization=None, authorization_scopes=None, authorizer_id=None, http_method=None, request_models=None, request_parameters=None, request_validator_id=None, resource_id=None, rest_api=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a HTTP Method for an API Gateway Resource.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] api_key_required: Specify if the method requires an API key
        :param pulumi.Input[str] authorization: The type of authorization used for the method (`NONE`, `CUSTOM`, `AWS_IAM`, `COGNITO_USER_POOLS`)
        :param pulumi.Input[list] authorization_scopes: The authorization scopes used when the authorization is `COGNITO_USER_POOLS`
        :param pulumi.Input[str] authorizer_id: The authorizer id to be used when the authorization is `CUSTOM` or `COGNITO_USER_POOLS`
        :param pulumi.Input[str] http_method: The HTTP Method (`GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `OPTIONS`, `ANY`)
        :param pulumi.Input[dict] request_models: A map of the API models used for the request's content type
               where key is the content type (e.g. `application/json`)
               and value is either `Error`, `Empty` (built-in models) or `apigateway.Model`'s `name`.
        :param pulumi.Input[dict] request_parameters: A map of request query string parameters and headers that should be passed to the integration.
               For example: `request_parameters = {"method.request.header.X-Some-Header" = true "method.request.querystring.some-query-param" = true}` would define that the header `X-Some-Header` and the query string `some-query-param` must be provided in the request
        :param pulumi.Input[str] request_validator_id: The ID of a `apigateway.RequestValidator`
        :param pulumi.Input[str] resource_id: The API resource ID
        :param pulumi.Input[str] rest_api: The ID of the associated REST API

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/api_gateway_method.html.markdown.
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

            __props__['api_key_required'] = api_key_required
            if authorization is None:
                raise TypeError("Missing required property 'authorization'")
            __props__['authorization'] = authorization
            __props__['authorization_scopes'] = authorization_scopes
            __props__['authorizer_id'] = authorizer_id
            if http_method is None:
                raise TypeError("Missing required property 'http_method'")
            __props__['http_method'] = http_method
            __props__['request_models'] = request_models
            __props__['request_parameters'] = request_parameters
            __props__['request_validator_id'] = request_validator_id
            if resource_id is None:
                raise TypeError("Missing required property 'resource_id'")
            __props__['resource_id'] = resource_id
            if rest_api is None:
                raise TypeError("Missing required property 'rest_api'")
            __props__['rest_api'] = rest_api
        super(Method, __self__).__init__(
            'aws:apigateway/method:Method',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, api_key_required=None, authorization=None, authorization_scopes=None, authorizer_id=None, http_method=None, request_models=None, request_parameters=None, request_validator_id=None, resource_id=None, rest_api=None):
        """
        Get an existing Method resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] api_key_required: Specify if the method requires an API key
        :param pulumi.Input[str] authorization: The type of authorization used for the method (`NONE`, `CUSTOM`, `AWS_IAM`, `COGNITO_USER_POOLS`)
        :param pulumi.Input[list] authorization_scopes: The authorization scopes used when the authorization is `COGNITO_USER_POOLS`
        :param pulumi.Input[str] authorizer_id: The authorizer id to be used when the authorization is `CUSTOM` or `COGNITO_USER_POOLS`
        :param pulumi.Input[str] http_method: The HTTP Method (`GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `OPTIONS`, `ANY`)
        :param pulumi.Input[dict] request_models: A map of the API models used for the request's content type
               where key is the content type (e.g. `application/json`)
               and value is either `Error`, `Empty` (built-in models) or `apigateway.Model`'s `name`.
        :param pulumi.Input[dict] request_parameters: A map of request query string parameters and headers that should be passed to the integration.
               For example: `request_parameters = {"method.request.header.X-Some-Header" = true "method.request.querystring.some-query-param" = true}` would define that the header `X-Some-Header` and the query string `some-query-param` must be provided in the request
        :param pulumi.Input[str] request_validator_id: The ID of a `apigateway.RequestValidator`
        :param pulumi.Input[str] resource_id: The API resource ID
        :param pulumi.Input[str] rest_api: The ID of the associated REST API

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/api_gateway_method.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["api_key_required"] = api_key_required
        __props__["authorization"] = authorization
        __props__["authorization_scopes"] = authorization_scopes
        __props__["authorizer_id"] = authorizer_id
        __props__["http_method"] = http_method
        __props__["request_models"] = request_models
        __props__["request_parameters"] = request_parameters
        __props__["request_validator_id"] = request_validator_id
        __props__["resource_id"] = resource_id
        __props__["rest_api"] = rest_api
        return Method(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

