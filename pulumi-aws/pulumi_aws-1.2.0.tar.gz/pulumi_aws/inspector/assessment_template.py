# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class AssessmentTemplate(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The template assessment ARN.
    """
    duration: pulumi.Output[float]
    """
    The duration of the inspector run.
    """
    name: pulumi.Output[str]
    """
    The name of the assessment template.
    """
    rules_package_arns: pulumi.Output[list]
    """
    The rules to be used during the run.
    """
    target_arn: pulumi.Output[str]
    """
    The assessment target ARN to attach the template to.
    """
    def __init__(__self__, resource_name, opts=None, duration=None, name=None, rules_package_arns=None, target_arn=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a Inspector assessment template
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] duration: The duration of the inspector run.
        :param pulumi.Input[str] name: The name of the assessment template.
        :param pulumi.Input[list] rules_package_arns: The rules to be used during the run.
        :param pulumi.Input[str] target_arn: The assessment target ARN to attach the template to.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/inspector_assessment_template.html.markdown.
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

            if duration is None:
                raise TypeError("Missing required property 'duration'")
            __props__['duration'] = duration
            __props__['name'] = name
            if rules_package_arns is None:
                raise TypeError("Missing required property 'rules_package_arns'")
            __props__['rules_package_arns'] = rules_package_arns
            if target_arn is None:
                raise TypeError("Missing required property 'target_arn'")
            __props__['target_arn'] = target_arn
            __props__['arn'] = None
        super(AssessmentTemplate, __self__).__init__(
            'aws:inspector/assessmentTemplate:AssessmentTemplate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, duration=None, name=None, rules_package_arns=None, target_arn=None):
        """
        Get an existing AssessmentTemplate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The template assessment ARN.
        :param pulumi.Input[float] duration: The duration of the inspector run.
        :param pulumi.Input[str] name: The name of the assessment template.
        :param pulumi.Input[list] rules_package_arns: The rules to be used during the run.
        :param pulumi.Input[str] target_arn: The assessment target ARN to attach the template to.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/inspector_assessment_template.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["arn"] = arn
        __props__["duration"] = duration
        __props__["name"] = name
        __props__["rules_package_arns"] = rules_package_arns
        __props__["target_arn"] = target_arn
        return AssessmentTemplate(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

