# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Cluster(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The Amazon Resource Name (ARN) of the cluster.
    """
    certificate_authority: pulumi.Output[dict]
    """
    Nested attribute containing `certificate-authority-data` for your cluster.
    
      * `data` (`str`) - The base64 encoded certificate data required to communicate with your cluster. Add this to the `certificate-authority-data` section of the `kubeconfig` file for your cluster.
    """
    created_at: pulumi.Output[str]
    enabled_cluster_log_types: pulumi.Output[list]
    """
    A list of the desired control plane logging to enable. For more information, see [Amazon EKS Control Plane Logging](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html)
    """
    endpoint: pulumi.Output[str]
    """
    The endpoint for your Kubernetes API server.
    """
    identities: pulumi.Output[list]
    """
    Nested attribute containing identity provider information for your cluster. Only available on Kubernetes version 1.13 and 1.14 clusters created or upgraded on or after September 3, 2019.
    
      * `oidcs` (`list`) - Nested attribute containing [OpenID Connect](https://openid.net/connect/) identity provider information for the cluster.
    
        * `issuer` (`str`) - Issuer URL for the OpenID Connect identity provider.
    """
    name: pulumi.Output[str]
    """
    Name of the cluster.
    """
    platform_version: pulumi.Output[str]
    """
    The platform version for the cluster.
    """
    role_arn: pulumi.Output[str]
    """
    The Amazon Resource Name (ARN) of the IAM role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf.
    """
    status: pulumi.Output[str]
    """
    The status of the EKS cluster. One of `CREATING`, `ACTIVE`, `DELETING`, `FAILED`. 
    """
    version: pulumi.Output[str]
    """
    Desired Kubernetes master version. If you do not specify a value, the latest available version at resource creation is used and no upgrades will occur except those automatically triggered by EKS. The value must be configured and increased to upgrade the version when desired. Downgrades are not supported by EKS.
    """
    vpc_config: pulumi.Output[dict]
    """
    Nested argument for the VPC associated with your cluster. Amazon EKS VPC resources have specific requirements to work properly with Kubernetes. For more information, see [Cluster VPC Considerations](https://docs.aws.amazon.com/eks/latest/userguide/network_reqs.html) and [Cluster Security Group Considerations](https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html) in the Amazon EKS User Guide. Configuration detailed below.
    
      * `endpointPrivateAccess` (`bool`) - Indicates whether or not the Amazon EKS private API server endpoint is enabled. Default is `false`.
      * `endpointPublicAccess` (`bool`) - Indicates whether or not the Amazon EKS public API server endpoint is enabled. Default is `true`.
      * `security_group_ids` (`list`) - List of security group IDs for the cross-account elastic network interfaces that Amazon EKS creates to use to allow communication between your worker nodes and the Kubernetes control plane.
      * `subnet_ids` (`list`) - List of subnet IDs. Must be in at least two different availability zones. Amazon EKS creates cross-account elastic network interfaces in these subnets to allow communication between your worker nodes and the Kubernetes control plane.
      * `vpc_id` (`str`) - The VPC associated with your cluster.
    """
    def __init__(__self__, resource_name, opts=None, enabled_cluster_log_types=None, name=None, role_arn=None, version=None, vpc_config=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an EKS Cluster.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] enabled_cluster_log_types: A list of the desired control plane logging to enable. For more information, see [Amazon EKS Control Plane Logging](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html)
        :param pulumi.Input[str] name: Name of the cluster.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the IAM role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf.
        :param pulumi.Input[str] version: Desired Kubernetes master version. If you do not specify a value, the latest available version at resource creation is used and no upgrades will occur except those automatically triggered by EKS. The value must be configured and increased to upgrade the version when desired. Downgrades are not supported by EKS.
        :param pulumi.Input[dict] vpc_config: Nested argument for the VPC associated with your cluster. Amazon EKS VPC resources have specific requirements to work properly with Kubernetes. For more information, see [Cluster VPC Considerations](https://docs.aws.amazon.com/eks/latest/userguide/network_reqs.html) and [Cluster Security Group Considerations](https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html) in the Amazon EKS User Guide. Configuration detailed below.
        
        The **vpc_config** object supports the following:
        
          * `endpointPrivateAccess` (`pulumi.Input[bool]`) - Indicates whether or not the Amazon EKS private API server endpoint is enabled. Default is `false`.
          * `endpointPublicAccess` (`pulumi.Input[bool]`) - Indicates whether or not the Amazon EKS public API server endpoint is enabled. Default is `true`.
          * `security_group_ids` (`pulumi.Input[list]`) - List of security group IDs for the cross-account elastic network interfaces that Amazon EKS creates to use to allow communication between your worker nodes and the Kubernetes control plane.
          * `subnet_ids` (`pulumi.Input[list]`) - List of subnet IDs. Must be in at least two different availability zones. Amazon EKS creates cross-account elastic network interfaces in these subnets to allow communication between your worker nodes and the Kubernetes control plane.
          * `vpc_id` (`pulumi.Input[str]`) - The VPC associated with your cluster.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/eks_cluster.html.markdown.
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

            __props__['enabled_cluster_log_types'] = enabled_cluster_log_types
            __props__['name'] = name
            if role_arn is None:
                raise TypeError("Missing required property 'role_arn'")
            __props__['role_arn'] = role_arn
            __props__['version'] = version
            if vpc_config is None:
                raise TypeError("Missing required property 'vpc_config'")
            __props__['vpc_config'] = vpc_config
            __props__['arn'] = None
            __props__['certificate_authority'] = None
            __props__['created_at'] = None
            __props__['endpoint'] = None
            __props__['identities'] = None
            __props__['platform_version'] = None
            __props__['status'] = None
        super(Cluster, __self__).__init__(
            'aws:eks/cluster:Cluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, certificate_authority=None, created_at=None, enabled_cluster_log_types=None, endpoint=None, identities=None, name=None, platform_version=None, role_arn=None, status=None, version=None, vpc_config=None):
        """
        Get an existing Cluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the cluster.
        :param pulumi.Input[dict] certificate_authority: Nested attribute containing `certificate-authority-data` for your cluster.
        :param pulumi.Input[list] enabled_cluster_log_types: A list of the desired control plane logging to enable. For more information, see [Amazon EKS Control Plane Logging](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html)
        :param pulumi.Input[str] endpoint: The endpoint for your Kubernetes API server.
        :param pulumi.Input[list] identities: Nested attribute containing identity provider information for your cluster. Only available on Kubernetes version 1.13 and 1.14 clusters created or upgraded on or after September 3, 2019.
        :param pulumi.Input[str] name: Name of the cluster.
        :param pulumi.Input[str] platform_version: The platform version for the cluster.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the IAM role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf.
        :param pulumi.Input[str] status: The status of the EKS cluster. One of `CREATING`, `ACTIVE`, `DELETING`, `FAILED`. 
        :param pulumi.Input[str] version: Desired Kubernetes master version. If you do not specify a value, the latest available version at resource creation is used and no upgrades will occur except those automatically triggered by EKS. The value must be configured and increased to upgrade the version when desired. Downgrades are not supported by EKS.
        :param pulumi.Input[dict] vpc_config: Nested argument for the VPC associated with your cluster. Amazon EKS VPC resources have specific requirements to work properly with Kubernetes. For more information, see [Cluster VPC Considerations](https://docs.aws.amazon.com/eks/latest/userguide/network_reqs.html) and [Cluster Security Group Considerations](https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html) in the Amazon EKS User Guide. Configuration detailed below.
        
        The **certificate_authority** object supports the following:
        
          * `data` (`pulumi.Input[str]`) - The base64 encoded certificate data required to communicate with your cluster. Add this to the `certificate-authority-data` section of the `kubeconfig` file for your cluster.
        
        The **identities** object supports the following:
        
          * `oidcs` (`pulumi.Input[list]`) - Nested attribute containing [OpenID Connect](https://openid.net/connect/) identity provider information for the cluster.
        
            * `issuer` (`pulumi.Input[str]`) - Issuer URL for the OpenID Connect identity provider.
        
        The **vpc_config** object supports the following:
        
          * `endpointPrivateAccess` (`pulumi.Input[bool]`) - Indicates whether or not the Amazon EKS private API server endpoint is enabled. Default is `false`.
          * `endpointPublicAccess` (`pulumi.Input[bool]`) - Indicates whether or not the Amazon EKS public API server endpoint is enabled. Default is `true`.
          * `security_group_ids` (`pulumi.Input[list]`) - List of security group IDs for the cross-account elastic network interfaces that Amazon EKS creates to use to allow communication between your worker nodes and the Kubernetes control plane.
          * `subnet_ids` (`pulumi.Input[list]`) - List of subnet IDs. Must be in at least two different availability zones. Amazon EKS creates cross-account elastic network interfaces in these subnets to allow communication between your worker nodes and the Kubernetes control plane.
          * `vpc_id` (`pulumi.Input[str]`) - The VPC associated with your cluster.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/eks_cluster.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["arn"] = arn
        __props__["certificate_authority"] = certificate_authority
        __props__["created_at"] = created_at
        __props__["enabled_cluster_log_types"] = enabled_cluster_log_types
        __props__["endpoint"] = endpoint
        __props__["identities"] = identities
        __props__["name"] = name
        __props__["platform_version"] = platform_version
        __props__["role_arn"] = role_arn
        __props__["status"] = status
        __props__["version"] = version
        __props__["vpc_config"] = vpc_config
        return Cluster(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

