# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetFunctionResult:
    """
    A collection of values returned by getFunction.
    """
    def __init__(__self__, arn=None, dead_letter_config=None, description=None, environment=None, function_name=None, handler=None, invoke_arn=None, kms_key_arn=None, last_modified=None, layers=None, memory_size=None, qualified_arn=None, qualifier=None, reserved_concurrent_executions=None, role=None, runtime=None, source_code_hash=None, source_code_size=None, tags=None, timeout=None, tracing_config=None, version=None, vpc_config=None, id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        __self__.arn = arn
        """
        Unqualified (no `:QUALIFIER` or `:VERSION` suffix) Amazon Resource Name (ARN) identifying your Lambda Function. See also `qualified_arn`.
        """
        if dead_letter_config and not isinstance(dead_letter_config, dict):
            raise TypeError("Expected argument 'dead_letter_config' to be a dict")
        __self__.dead_letter_config = dead_letter_config
        """
        Configure the function's *dead letter queue*.
        """
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        __self__.description = description
        """
        Description of what your Lambda Function does.
        """
        if environment and not isinstance(environment, dict):
            raise TypeError("Expected argument 'environment' to be a dict")
        __self__.environment = environment
        """
        The Lambda environment's configuration settings.
        """
        if function_name and not isinstance(function_name, str):
            raise TypeError("Expected argument 'function_name' to be a str")
        __self__.function_name = function_name
        if handler and not isinstance(handler, str):
            raise TypeError("Expected argument 'handler' to be a str")
        __self__.handler = handler
        """
        The function entrypoint in your code.
        """
        if invoke_arn and not isinstance(invoke_arn, str):
            raise TypeError("Expected argument 'invoke_arn' to be a str")
        __self__.invoke_arn = invoke_arn
        """
        The ARN to be used for invoking Lambda Function from API Gateway.
        """
        if kms_key_arn and not isinstance(kms_key_arn, str):
            raise TypeError("Expected argument 'kms_key_arn' to be a str")
        __self__.kms_key_arn = kms_key_arn
        """
        The ARN for the KMS encryption key.
        """
        if last_modified and not isinstance(last_modified, str):
            raise TypeError("Expected argument 'last_modified' to be a str")
        __self__.last_modified = last_modified
        """
        The date this resource was last modified.
        """
        if layers and not isinstance(layers, list):
            raise TypeError("Expected argument 'layers' to be a list")
        __self__.layers = layers
        """
        A list of Lambda Layer ARNs attached to your Lambda Function.
        """
        if memory_size and not isinstance(memory_size, float):
            raise TypeError("Expected argument 'memory_size' to be a float")
        __self__.memory_size = memory_size
        """
        Amount of memory in MB your Lambda Function can use at runtime.
        """
        if qualified_arn and not isinstance(qualified_arn, str):
            raise TypeError("Expected argument 'qualified_arn' to be a str")
        __self__.qualified_arn = qualified_arn
        """
        Qualified (`:QUALIFIER` or `:VERSION` suffix) Amazon Resource Name (ARN) identifying your Lambda Function. See also `arn`.
        """
        if qualifier and not isinstance(qualifier, str):
            raise TypeError("Expected argument 'qualifier' to be a str")
        __self__.qualifier = qualifier
        if reserved_concurrent_executions and not isinstance(reserved_concurrent_executions, float):
            raise TypeError("Expected argument 'reserved_concurrent_executions' to be a float")
        __self__.reserved_concurrent_executions = reserved_concurrent_executions
        """
        The amount of reserved concurrent executions for this lambda function or `-1` if unreserved.
        """
        if role and not isinstance(role, str):
            raise TypeError("Expected argument 'role' to be a str")
        __self__.role = role
        """
        IAM role attached to the Lambda Function.
        """
        if runtime and not isinstance(runtime, str):
            raise TypeError("Expected argument 'runtime' to be a str")
        __self__.runtime = runtime
        """
        The runtime environment for the Lambda function..
        """
        if source_code_hash and not isinstance(source_code_hash, str):
            raise TypeError("Expected argument 'source_code_hash' to be a str")
        __self__.source_code_hash = source_code_hash
        """
        Base64-encoded representation of raw SHA-256 sum of the zip file.
        """
        if source_code_size and not isinstance(source_code_size, float):
            raise TypeError("Expected argument 'source_code_size' to be a float")
        __self__.source_code_size = source_code_size
        """
        The size in bytes of the function .zip file.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        if timeout and not isinstance(timeout, float):
            raise TypeError("Expected argument 'timeout' to be a float")
        __self__.timeout = timeout
        """
        The function execution time at which Lambda should terminate the function.
        """
        if tracing_config and not isinstance(tracing_config, dict):
            raise TypeError("Expected argument 'tracing_config' to be a dict")
        __self__.tracing_config = tracing_config
        """
        Tracing settings of the function.
        """
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        __self__.version = version
        """
        The version of the Lambda function.
        """
        if vpc_config and not isinstance(vpc_config, dict):
            raise TypeError("Expected argument 'vpc_config' to be a dict")
        __self__.vpc_config = vpc_config
        """
        VPC configuration associated with your Lambda function.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
class AwaitableGetFunctionResult(GetFunctionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFunctionResult(
            arn=self.arn,
            dead_letter_config=self.dead_letter_config,
            description=self.description,
            environment=self.environment,
            function_name=self.function_name,
            handler=self.handler,
            invoke_arn=self.invoke_arn,
            kms_key_arn=self.kms_key_arn,
            last_modified=self.last_modified,
            layers=self.layers,
            memory_size=self.memory_size,
            qualified_arn=self.qualified_arn,
            qualifier=self.qualifier,
            reserved_concurrent_executions=self.reserved_concurrent_executions,
            role=self.role,
            runtime=self.runtime,
            source_code_hash=self.source_code_hash,
            source_code_size=self.source_code_size,
            tags=self.tags,
            timeout=self.timeout,
            tracing_config=self.tracing_config,
            version=self.version,
            vpc_config=self.vpc_config,
            id=self.id)

def get_function(function_name=None,qualifier=None,tags=None,opts=None):
    """
    Provides information about a Lambda Function.
    
    :param str function_name: Name of the lambda function.
    :param str qualifier: Alias name or version number of the lambda function. e.g. `$LATEST`, `my-alias`, or `1`

    > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/d/lambda_function.html.markdown.
    """
    __args__ = dict()

    __args__['functionName'] = function_name
    __args__['qualifier'] = qualifier
    __args__['tags'] = tags
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:lambda/getFunction:getFunction', __args__, opts=opts).value

    return AwaitableGetFunctionResult(
        arn=__ret__.get('arn'),
        dead_letter_config=__ret__.get('deadLetterConfig'),
        description=__ret__.get('description'),
        environment=__ret__.get('environment'),
        function_name=__ret__.get('functionName'),
        handler=__ret__.get('handler'),
        invoke_arn=__ret__.get('invokeArn'),
        kms_key_arn=__ret__.get('kmsKeyArn'),
        last_modified=__ret__.get('lastModified'),
        layers=__ret__.get('layers'),
        memory_size=__ret__.get('memorySize'),
        qualified_arn=__ret__.get('qualifiedArn'),
        qualifier=__ret__.get('qualifier'),
        reserved_concurrent_executions=__ret__.get('reservedConcurrentExecutions'),
        role=__ret__.get('role'),
        runtime=__ret__.get('runtime'),
        source_code_hash=__ret__.get('sourceCodeHash'),
        source_code_size=__ret__.get('sourceCodeSize'),
        tags=__ret__.get('tags'),
        timeout=__ret__.get('timeout'),
        tracing_config=__ret__.get('tracingConfig'),
        version=__ret__.get('version'),
        vpc_config=__ret__.get('vpcConfig'),
        id=__ret__.get('id'))
