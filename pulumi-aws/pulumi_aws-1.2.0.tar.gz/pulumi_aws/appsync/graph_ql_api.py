# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GraphQLApi(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The ARN
    """
    authentication_type: pulumi.Output[str]
    """
    The authentication type. Valid values: `API_KEY`, `AWS_IAM`, `AMAZON_COGNITO_USER_POOLS`, `OPENID_CONNECT`
    """
    log_config: pulumi.Output[dict]
    """
    Nested argument containing logging configuration. Defined below.
    
      * `cloudwatchLogsRoleArn` (`str`) - Amazon Resource Name of the service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your account.
      * `fieldLogLevel` (`str`) - Field logging level. Valid values: `ALL`, `ERROR`, `NONE`.
    """
    name: pulumi.Output[str]
    """
    A user-supplied name for the GraphqlApi.
    """
    openid_connect_config: pulumi.Output[dict]
    """
    Nested argument containing OpenID Connect configuration. Defined below.
    
      * `authTtl` (`float`) - Number of milliseconds a token is valid after being authenticated.
      * `clientId` (`str`) - Client identifier of the Relying party at the OpenID identity provider. This identifier is typically obtained when the Relying party is registered with the OpenID identity provider. You can specify a regular expression so the AWS AppSync can validate against multiple client identifiers at a time.
      * `iatTtl` (`float`) - Number of milliseconds a token is valid after being issued to a user.
      * `issuer` (`str`) - Issuer for the OpenID Connect configuration. The issuer returned by discovery MUST exactly match the value of iss in the ID Token.
    """
    schema: pulumi.Output[str]
    """
    The schema definition, in GraphQL schema language format. This provider cannot perform drift detection of this configuration.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    uris: pulumi.Output[dict]
    """
    Map of URIs associated with the API. e.g. `uris["GRAPHQL"] = https://ID.appsync-api.REGION.amazonaws.com/graphql`
    """
    user_pool_config: pulumi.Output[dict]
    """
    The Amazon Cognito User Pool configuration. Defined below.
    
      * `appIdClientRegex` (`str`) - A regular expression for validating the incoming Amazon Cognito User Pool app client ID.
      * `awsRegion` (`str`) - The AWS region in which the user pool was created.
      * `defaultAction` (`str`) - The action that you want your GraphQL API to take when a request that uses Amazon Cognito User Pool authentication doesn't match the Amazon Cognito User Pool configuration. Valid: `ALLOW` and `DENY`
      * `userPoolId` (`str`) - The user pool ID.
    """
    def __init__(__self__, resource_name, opts=None, authentication_type=None, log_config=None, name=None, openid_connect_config=None, schema=None, tags=None, user_pool_config=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an AppSync GraphQL API.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authentication_type: The authentication type. Valid values: `API_KEY`, `AWS_IAM`, `AMAZON_COGNITO_USER_POOLS`, `OPENID_CONNECT`
        :param pulumi.Input[dict] log_config: Nested argument containing logging configuration. Defined below.
        :param pulumi.Input[str] name: A user-supplied name for the GraphqlApi.
        :param pulumi.Input[dict] openid_connect_config: Nested argument containing OpenID Connect configuration. Defined below.
        :param pulumi.Input[str] schema: The schema definition, in GraphQL schema language format. This provider cannot perform drift detection of this configuration.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[dict] user_pool_config: The Amazon Cognito User Pool configuration. Defined below.
        
        The **log_config** object supports the following:
        
          * `cloudwatchLogsRoleArn` (`pulumi.Input[str]`) - Amazon Resource Name of the service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your account.
          * `fieldLogLevel` (`pulumi.Input[str]`) - Field logging level. Valid values: `ALL`, `ERROR`, `NONE`.
        
        The **openid_connect_config** object supports the following:
        
          * `authTtl` (`pulumi.Input[float]`) - Number of milliseconds a token is valid after being authenticated.
          * `clientId` (`pulumi.Input[str]`) - Client identifier of the Relying party at the OpenID identity provider. This identifier is typically obtained when the Relying party is registered with the OpenID identity provider. You can specify a regular expression so the AWS AppSync can validate against multiple client identifiers at a time.
          * `iatTtl` (`pulumi.Input[float]`) - Number of milliseconds a token is valid after being issued to a user.
          * `issuer` (`pulumi.Input[str]`) - Issuer for the OpenID Connect configuration. The issuer returned by discovery MUST exactly match the value of iss in the ID Token.
        
        The **user_pool_config** object supports the following:
        
          * `appIdClientRegex` (`pulumi.Input[str]`) - A regular expression for validating the incoming Amazon Cognito User Pool app client ID.
          * `awsRegion` (`pulumi.Input[str]`) - The AWS region in which the user pool was created.
          * `defaultAction` (`pulumi.Input[str]`) - The action that you want your GraphQL API to take when a request that uses Amazon Cognito User Pool authentication doesn't match the Amazon Cognito User Pool configuration. Valid: `ALLOW` and `DENY`
          * `userPoolId` (`pulumi.Input[str]`) - The user pool ID.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/appsync_graphql_api.html.markdown.
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

            if authentication_type is None:
                raise TypeError("Missing required property 'authentication_type'")
            __props__['authentication_type'] = authentication_type
            __props__['log_config'] = log_config
            __props__['name'] = name
            __props__['openid_connect_config'] = openid_connect_config
            __props__['schema'] = schema
            __props__['tags'] = tags
            __props__['user_pool_config'] = user_pool_config
            __props__['arn'] = None
            __props__['uris'] = None
        super(GraphQLApi, __self__).__init__(
            'aws:appsync/graphQLApi:GraphQLApi',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, authentication_type=None, log_config=None, name=None, openid_connect_config=None, schema=None, tags=None, uris=None, user_pool_config=None):
        """
        Get an existing GraphQLApi resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN
        :param pulumi.Input[str] authentication_type: The authentication type. Valid values: `API_KEY`, `AWS_IAM`, `AMAZON_COGNITO_USER_POOLS`, `OPENID_CONNECT`
        :param pulumi.Input[dict] log_config: Nested argument containing logging configuration. Defined below.
        :param pulumi.Input[str] name: A user-supplied name for the GraphqlApi.
        :param pulumi.Input[dict] openid_connect_config: Nested argument containing OpenID Connect configuration. Defined below.
        :param pulumi.Input[str] schema: The schema definition, in GraphQL schema language format. This provider cannot perform drift detection of this configuration.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[dict] uris: Map of URIs associated with the API. e.g. `uris["GRAPHQL"] = https://ID.appsync-api.REGION.amazonaws.com/graphql`
        :param pulumi.Input[dict] user_pool_config: The Amazon Cognito User Pool configuration. Defined below.
        
        The **log_config** object supports the following:
        
          * `cloudwatchLogsRoleArn` (`pulumi.Input[str]`) - Amazon Resource Name of the service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your account.
          * `fieldLogLevel` (`pulumi.Input[str]`) - Field logging level. Valid values: `ALL`, `ERROR`, `NONE`.
        
        The **openid_connect_config** object supports the following:
        
          * `authTtl` (`pulumi.Input[float]`) - Number of milliseconds a token is valid after being authenticated.
          * `clientId` (`pulumi.Input[str]`) - Client identifier of the Relying party at the OpenID identity provider. This identifier is typically obtained when the Relying party is registered with the OpenID identity provider. You can specify a regular expression so the AWS AppSync can validate against multiple client identifiers at a time.
          * `iatTtl` (`pulumi.Input[float]`) - Number of milliseconds a token is valid after being issued to a user.
          * `issuer` (`pulumi.Input[str]`) - Issuer for the OpenID Connect configuration. The issuer returned by discovery MUST exactly match the value of iss in the ID Token.
        
        The **user_pool_config** object supports the following:
        
          * `appIdClientRegex` (`pulumi.Input[str]`) - A regular expression for validating the incoming Amazon Cognito User Pool app client ID.
          * `awsRegion` (`pulumi.Input[str]`) - The AWS region in which the user pool was created.
          * `defaultAction` (`pulumi.Input[str]`) - The action that you want your GraphQL API to take when a request that uses Amazon Cognito User Pool authentication doesn't match the Amazon Cognito User Pool configuration. Valid: `ALLOW` and `DENY`
          * `userPoolId` (`pulumi.Input[str]`) - The user pool ID.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/appsync_graphql_api.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["arn"] = arn
        __props__["authentication_type"] = authentication_type
        __props__["log_config"] = log_config
        __props__["name"] = name
        __props__["openid_connect_config"] = openid_connect_config
        __props__["schema"] = schema
        __props__["tags"] = tags
        __props__["uris"] = uris
        __props__["user_pool_config"] = user_pool_config
        return GraphQLApi(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

