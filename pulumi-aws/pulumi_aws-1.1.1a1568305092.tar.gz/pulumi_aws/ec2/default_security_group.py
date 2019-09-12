# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class DefaultSecurityGroup(pulumi.CustomResource):
    arn: pulumi.Output[str]
    egress: pulumi.Output[list]
    """
    Can be specified multiple times for each
    egress rule. Each egress block supports fields documented below.
    
      * `cidr_blocks` (`list`)
      * `description` (`str`) - The description of the security group
      * `from_port` (`float`)
      * `ipv6_cidr_blocks` (`list`)
      * `prefix_list_ids` (`list`)
      * `protocol` (`str`)
      * `security_groups` (`list`)
      * `self` (`bool`)
      * `to_port` (`float`)
    """
    ingress: pulumi.Output[list]
    """
    Can be specified multiple times for each
    ingress rule. Each ingress block supports fields documented below.
    
      * `cidr_blocks` (`list`)
      * `description` (`str`) - The description of the security group
      * `from_port` (`float`)
      * `ipv6_cidr_blocks` (`list`)
      * `prefix_list_ids` (`list`)
      * `protocol` (`str`)
      * `security_groups` (`list`)
      * `self` (`bool`)
      * `to_port` (`float`)
    """
    name: pulumi.Output[str]
    """
    The name of the security group
    """
    owner_id: pulumi.Output[str]
    """
    The owner ID.
    """
    revoke_rules_on_delete: pulumi.Output[bool]
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    vpc_id: pulumi.Output[str]
    """
    The VPC ID. **Note that changing
    the `vpc_id` will _not_ restore any default security group rules that were
    modified, added, or removed.** It will be left in its current state
    """
    def __init__(__self__, resource_name, opts=None, egress=None, ingress=None, revoke_rules_on_delete=None, tags=None, vpc_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a resource to manage the default AWS Security Group.
        
        For EC2 Classic accounts, each region comes with a Default Security Group.
        Additionally, each VPC created in AWS comes with a Default Security Group that can be managed, but not
        destroyed. **This is an advanced resource**, and has special caveats to be aware
        of when using it. Please read this document in its entirety before using this
        resource.
        
        The `ec2.DefaultSecurityGroup` behaves differently from normal resources, in that
        this provider does not _create_ this resource, but instead "adopts" it
        into management. We can do this because these default security groups cannot be
        destroyed, and are created with a known set of default ingress/egress rules.
        
        When this provider first adopts the Default Security Group, it **immediately removes all
        ingress and egress rules in the Security Group**. It then proceeds to create any rules specified in the
        configuration. This step is required so that only the rules specified in the
        configuration are created.
        
        This resource treats its inline rules as absolute; only the rules defined
        inline are created, and any additions/removals external to this resource will
        result in diff shown. For these reasons, this resource is incompatible with the
        `ec2.SecurityGroupRule` resource.
        
        For more information about Default Security Groups, see the AWS Documentation on
        [Default Security Groups][aws-default-security-groups].
        
        ## Usage
        
        With the exceptions mentioned above, `ec2.DefaultSecurityGroup` should
        identical behavior to `ec2.SecurityGroup`. Please consult [AWS_SECURITY_GROUP](https://www.terraform.io/docs/providers/aws/r/security_group.html)
        for further usage documentation.
        
        ### Removing `ec2.DefaultSecurityGroup` from your configuration
        
        Each AWS VPC (or region, if using EC2 Classic) comes with a Default Security
        Group that cannot be deleted. The `ec2.DefaultSecurityGroup` allows you to
        manage this Security Group, but this provider cannot destroy it. Removing this resource
        from your configuration will remove it from your statefile and management, but
        will not destroy the Security Group. All ingress or egress rules will be left as
        they are at the time of removal. You can resume managing them via the AWS Console.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] egress: Can be specified multiple times for each
               egress rule. Each egress block supports fields documented below.
        :param pulumi.Input[list] ingress: Can be specified multiple times for each
               ingress rule. Each ingress block supports fields documented below.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] vpc_id: The VPC ID. **Note that changing
               the `vpc_id` will _not_ restore any default security group rules that were
               modified, added, or removed.** It will be left in its current state
        
        The **egress** object supports the following:
        
          * `cidr_blocks` (`pulumi.Input[list]`)
          * `description` (`pulumi.Input[str]`) - The description of the security group
          * `from_port` (`pulumi.Input[float]`)
          * `ipv6_cidr_blocks` (`pulumi.Input[list]`)
          * `prefix_list_ids` (`pulumi.Input[list]`)
          * `protocol` (`pulumi.Input[str]`)
          * `security_groups` (`pulumi.Input[list]`)
          * `self` (`pulumi.Input[bool]`)
          * `to_port` (`pulumi.Input[float]`)
        
        The **ingress** object supports the following:
        
          * `cidr_blocks` (`pulumi.Input[list]`)
          * `description` (`pulumi.Input[str]`) - The description of the security group
          * `from_port` (`pulumi.Input[float]`)
          * `ipv6_cidr_blocks` (`pulumi.Input[list]`)
          * `prefix_list_ids` (`pulumi.Input[list]`)
          * `protocol` (`pulumi.Input[str]`)
          * `security_groups` (`pulumi.Input[list]`)
          * `self` (`pulumi.Input[bool]`)
          * `to_port` (`pulumi.Input[float]`)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/default_security_group.html.markdown.
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

            __props__['egress'] = egress
            __props__['ingress'] = ingress
            __props__['revoke_rules_on_delete'] = revoke_rules_on_delete
            __props__['tags'] = tags
            __props__['vpc_id'] = vpc_id
            __props__['arn'] = None
            __props__['name'] = None
            __props__['owner_id'] = None
        super(DefaultSecurityGroup, __self__).__init__(
            'aws:ec2/defaultSecurityGroup:DefaultSecurityGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, egress=None, ingress=None, name=None, owner_id=None, revoke_rules_on_delete=None, tags=None, vpc_id=None):
        """
        Get an existing DefaultSecurityGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] egress: Can be specified multiple times for each
               egress rule. Each egress block supports fields documented below.
        :param pulumi.Input[list] ingress: Can be specified multiple times for each
               ingress rule. Each ingress block supports fields documented below.
        :param pulumi.Input[str] name: The name of the security group
        :param pulumi.Input[str] owner_id: The owner ID.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] vpc_id: The VPC ID. **Note that changing
               the `vpc_id` will _not_ restore any default security group rules that were
               modified, added, or removed.** It will be left in its current state
        
        The **egress** object supports the following:
        
          * `cidr_blocks` (`pulumi.Input[list]`)
          * `description` (`pulumi.Input[str]`) - The description of the security group
          * `from_port` (`pulumi.Input[float]`)
          * `ipv6_cidr_blocks` (`pulumi.Input[list]`)
          * `prefix_list_ids` (`pulumi.Input[list]`)
          * `protocol` (`pulumi.Input[str]`)
          * `security_groups` (`pulumi.Input[list]`)
          * `self` (`pulumi.Input[bool]`)
          * `to_port` (`pulumi.Input[float]`)
        
        The **ingress** object supports the following:
        
          * `cidr_blocks` (`pulumi.Input[list]`)
          * `description` (`pulumi.Input[str]`) - The description of the security group
          * `from_port` (`pulumi.Input[float]`)
          * `ipv6_cidr_blocks` (`pulumi.Input[list]`)
          * `prefix_list_ids` (`pulumi.Input[list]`)
          * `protocol` (`pulumi.Input[str]`)
          * `security_groups` (`pulumi.Input[list]`)
          * `self` (`pulumi.Input[bool]`)
          * `to_port` (`pulumi.Input[float]`)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/default_security_group.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["arn"] = arn
        __props__["egress"] = egress
        __props__["ingress"] = ingress
        __props__["name"] = name
        __props__["owner_id"] = owner_id
        __props__["revoke_rules_on_delete"] = revoke_rules_on_delete
        __props__["tags"] = tags
        __props__["vpc_id"] = vpc_id
        return DefaultSecurityGroup(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

