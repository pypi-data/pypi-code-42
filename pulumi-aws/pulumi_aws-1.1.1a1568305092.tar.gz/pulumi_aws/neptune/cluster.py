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
    apply_immediately: pulumi.Output[bool]
    """
    Specifies whether any cluster modifications are applied immediately, or during the next maintenance window. Default is `false`.
    """
    arn: pulumi.Output[str]
    """
    The Neptune Cluster Amazon Resource Name (ARN)
    """
    availability_zones: pulumi.Output[list]
    """
    A list of EC2 Availability Zones that instances in the Neptune cluster can be created in.
    """
    backup_retention_period: pulumi.Output[float]
    """
    The days to retain backups for. Default `1`
    """
    cluster_identifier: pulumi.Output[str]
    """
    The cluster identifier. If omitted, this provider will assign a random, unique identifier.
    """
    cluster_identifier_prefix: pulumi.Output[str]
    """
    Creates a unique cluster identifier beginning with the specified prefix. Conflicts with `cluster_identifier`.
    """
    cluster_members: pulumi.Output[list]
    """
    List of Neptune Instances that are a part of this cluster
    """
    cluster_resource_id: pulumi.Output[str]
    """
    The Neptune Cluster Resource ID
    """
    endpoint: pulumi.Output[str]
    """
    The DNS address of the Neptune instance
    """
    engine: pulumi.Output[str]
    """
    The name of the database engine to be used for this Neptune cluster. Defaults to `neptune`.
    """
    engine_version: pulumi.Output[str]
    """
    The database engine version.
    """
    final_snapshot_identifier: pulumi.Output[str]
    """
    The name of your final Neptune snapshot when this Neptune cluster is deleted. If omitted, no final snapshot will be made.
    """
    hosted_zone_id: pulumi.Output[str]
    """
    The Route53 Hosted Zone ID of the endpoint
    """
    iam_database_authentication_enabled: pulumi.Output[bool]
    """
    Specifies whether or mappings of AWS Identity and Access Management (IAM) accounts to database accounts is enabled.
    """
    iam_roles: pulumi.Output[list]
    """
    A List of ARNs for the IAM roles to associate to the Neptune Cluster.
    """
    kms_key_arn: pulumi.Output[str]
    """
    The ARN for the KMS encryption key. When specifying `kms_key_arn`, `storage_encrypted` needs to be set to true.
    """
    neptune_cluster_parameter_group_name: pulumi.Output[str]
    """
    A cluster parameter group to associate with the cluster.
    """
    neptune_subnet_group_name: pulumi.Output[str]
    """
    A Neptune subnet group to associate with this Neptune instance.
    """
    port: pulumi.Output[float]
    """
    The port on which the Neptune accepts connections. Default is `8182`.
    """
    preferred_backup_window: pulumi.Output[str]
    """
    The daily time range during which automated backups are created if automated backups are enabled using the BackupRetentionPeriod parameter. Time in UTC. Default: A 30-minute window selected at random from an 8-hour block of time per region. e.g. 04:00-09:00
    """
    preferred_maintenance_window: pulumi.Output[str]
    """
    The weekly time range during which system maintenance can occur, in (UTC) e.g. wed:04:00-wed:04:30
    """
    reader_endpoint: pulumi.Output[str]
    """
    A read-only endpoint for the Neptune cluster, automatically load-balanced across replicas
    """
    replication_source_identifier: pulumi.Output[str]
    """
    ARN of a source Neptune cluster or Neptune instance if this Neptune cluster is to be created as a Read Replica.
    """
    skip_final_snapshot: pulumi.Output[bool]
    """
    Determines whether a final Neptune snapshot is created before the Neptune cluster is deleted. If true is specified, no Neptune snapshot is created. If false is specified, a Neptune snapshot is created before the Neptune cluster is deleted, using the value from `final_snapshot_identifier`. Default is `false`.
    """
    snapshot_identifier: pulumi.Output[str]
    """
    Specifies whether or not to create this cluster from a snapshot. You can use either the name or ARN when specifying a Neptune cluster snapshot, or the ARN when specifying a Neptune snapshot.
    """
    storage_encrypted: pulumi.Output[bool]
    """
    Specifies whether the Neptune cluster is encrypted. The default is `false` if not specified.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the Neptune cluster.
    """
    vpc_security_group_ids: pulumi.Output[list]
    """
    List of VPC security groups to associate with the Cluster
    """
    def __init__(__self__, resource_name, opts=None, apply_immediately=None, availability_zones=None, backup_retention_period=None, cluster_identifier=None, cluster_identifier_prefix=None, engine=None, engine_version=None, final_snapshot_identifier=None, iam_database_authentication_enabled=None, iam_roles=None, kms_key_arn=None, neptune_cluster_parameter_group_name=None, neptune_subnet_group_name=None, port=None, preferred_backup_window=None, preferred_maintenance_window=None, replication_source_identifier=None, skip_final_snapshot=None, snapshot_identifier=None, storage_encrypted=None, tags=None, vpc_security_group_ids=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an Neptune Cluster Resource. A Cluster Resource defines attributes that are
        applied to the entire cluster of Neptune Cluster Instances.
        
        Changes to a Neptune Cluster can occur when you manually change a
        parameter, such as `backup_retention_period`, and are reflected in the next maintenance
        window. Because of this, this provider may report a difference in its planning
        phase because a modification has not yet taken place. You can use the
        `apply_immediately` flag to instruct the service to apply the change immediately
        (see documentation below).
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] apply_immediately: Specifies whether any cluster modifications are applied immediately, or during the next maintenance window. Default is `false`.
        :param pulumi.Input[list] availability_zones: A list of EC2 Availability Zones that instances in the Neptune cluster can be created in.
        :param pulumi.Input[float] backup_retention_period: The days to retain backups for. Default `1`
        :param pulumi.Input[str] cluster_identifier: The cluster identifier. If omitted, this provider will assign a random, unique identifier.
        :param pulumi.Input[str] cluster_identifier_prefix: Creates a unique cluster identifier beginning with the specified prefix. Conflicts with `cluster_identifier`.
        :param pulumi.Input[str] engine: The name of the database engine to be used for this Neptune cluster. Defaults to `neptune`.
        :param pulumi.Input[str] engine_version: The database engine version.
        :param pulumi.Input[str] final_snapshot_identifier: The name of your final Neptune snapshot when this Neptune cluster is deleted. If omitted, no final snapshot will be made.
        :param pulumi.Input[bool] iam_database_authentication_enabled: Specifies whether or mappings of AWS Identity and Access Management (IAM) accounts to database accounts is enabled.
        :param pulumi.Input[list] iam_roles: A List of ARNs for the IAM roles to associate to the Neptune Cluster.
        :param pulumi.Input[str] kms_key_arn: The ARN for the KMS encryption key. When specifying `kms_key_arn`, `storage_encrypted` needs to be set to true.
        :param pulumi.Input[str] neptune_cluster_parameter_group_name: A cluster parameter group to associate with the cluster.
        :param pulumi.Input[str] neptune_subnet_group_name: A Neptune subnet group to associate with this Neptune instance.
        :param pulumi.Input[float] port: The port on which the Neptune accepts connections. Default is `8182`.
        :param pulumi.Input[str] preferred_backup_window: The daily time range during which automated backups are created if automated backups are enabled using the BackupRetentionPeriod parameter. Time in UTC. Default: A 30-minute window selected at random from an 8-hour block of time per region. e.g. 04:00-09:00
        :param pulumi.Input[str] preferred_maintenance_window: The weekly time range during which system maintenance can occur, in (UTC) e.g. wed:04:00-wed:04:30
        :param pulumi.Input[str] replication_source_identifier: ARN of a source Neptune cluster or Neptune instance if this Neptune cluster is to be created as a Read Replica.
        :param pulumi.Input[bool] skip_final_snapshot: Determines whether a final Neptune snapshot is created before the Neptune cluster is deleted. If true is specified, no Neptune snapshot is created. If false is specified, a Neptune snapshot is created before the Neptune cluster is deleted, using the value from `final_snapshot_identifier`. Default is `false`.
        :param pulumi.Input[str] snapshot_identifier: Specifies whether or not to create this cluster from a snapshot. You can use either the name or ARN when specifying a Neptune cluster snapshot, or the ARN when specifying a Neptune snapshot.
        :param pulumi.Input[bool] storage_encrypted: Specifies whether the Neptune cluster is encrypted. The default is `false` if not specified.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the Neptune cluster.
        :param pulumi.Input[list] vpc_security_group_ids: List of VPC security groups to associate with the Cluster

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/neptune_cluster.html.markdown.
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

            __props__['apply_immediately'] = apply_immediately
            __props__['availability_zones'] = availability_zones
            __props__['backup_retention_period'] = backup_retention_period
            __props__['cluster_identifier'] = cluster_identifier
            __props__['cluster_identifier_prefix'] = cluster_identifier_prefix
            __props__['engine'] = engine
            __props__['engine_version'] = engine_version
            __props__['final_snapshot_identifier'] = final_snapshot_identifier
            __props__['iam_database_authentication_enabled'] = iam_database_authentication_enabled
            __props__['iam_roles'] = iam_roles
            __props__['kms_key_arn'] = kms_key_arn
            __props__['neptune_cluster_parameter_group_name'] = neptune_cluster_parameter_group_name
            __props__['neptune_subnet_group_name'] = neptune_subnet_group_name
            __props__['port'] = port
            __props__['preferred_backup_window'] = preferred_backup_window
            __props__['preferred_maintenance_window'] = preferred_maintenance_window
            __props__['replication_source_identifier'] = replication_source_identifier
            __props__['skip_final_snapshot'] = skip_final_snapshot
            __props__['snapshot_identifier'] = snapshot_identifier
            __props__['storage_encrypted'] = storage_encrypted
            __props__['tags'] = tags
            __props__['vpc_security_group_ids'] = vpc_security_group_ids
            __props__['arn'] = None
            __props__['cluster_members'] = None
            __props__['cluster_resource_id'] = None
            __props__['endpoint'] = None
            __props__['hosted_zone_id'] = None
            __props__['reader_endpoint'] = None
        super(Cluster, __self__).__init__(
            'aws:neptune/cluster:Cluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, apply_immediately=None, arn=None, availability_zones=None, backup_retention_period=None, cluster_identifier=None, cluster_identifier_prefix=None, cluster_members=None, cluster_resource_id=None, endpoint=None, engine=None, engine_version=None, final_snapshot_identifier=None, hosted_zone_id=None, iam_database_authentication_enabled=None, iam_roles=None, kms_key_arn=None, neptune_cluster_parameter_group_name=None, neptune_subnet_group_name=None, port=None, preferred_backup_window=None, preferred_maintenance_window=None, reader_endpoint=None, replication_source_identifier=None, skip_final_snapshot=None, snapshot_identifier=None, storage_encrypted=None, tags=None, vpc_security_group_ids=None):
        """
        Get an existing Cluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] apply_immediately: Specifies whether any cluster modifications are applied immediately, or during the next maintenance window. Default is `false`.
        :param pulumi.Input[str] arn: The Neptune Cluster Amazon Resource Name (ARN)
        :param pulumi.Input[list] availability_zones: A list of EC2 Availability Zones that instances in the Neptune cluster can be created in.
        :param pulumi.Input[float] backup_retention_period: The days to retain backups for. Default `1`
        :param pulumi.Input[str] cluster_identifier: The cluster identifier. If omitted, this provider will assign a random, unique identifier.
        :param pulumi.Input[str] cluster_identifier_prefix: Creates a unique cluster identifier beginning with the specified prefix. Conflicts with `cluster_identifier`.
        :param pulumi.Input[list] cluster_members: List of Neptune Instances that are a part of this cluster
        :param pulumi.Input[str] cluster_resource_id: The Neptune Cluster Resource ID
        :param pulumi.Input[str] endpoint: The DNS address of the Neptune instance
        :param pulumi.Input[str] engine: The name of the database engine to be used for this Neptune cluster. Defaults to `neptune`.
        :param pulumi.Input[str] engine_version: The database engine version.
        :param pulumi.Input[str] final_snapshot_identifier: The name of your final Neptune snapshot when this Neptune cluster is deleted. If omitted, no final snapshot will be made.
        :param pulumi.Input[str] hosted_zone_id: The Route53 Hosted Zone ID of the endpoint
        :param pulumi.Input[bool] iam_database_authentication_enabled: Specifies whether or mappings of AWS Identity and Access Management (IAM) accounts to database accounts is enabled.
        :param pulumi.Input[list] iam_roles: A List of ARNs for the IAM roles to associate to the Neptune Cluster.
        :param pulumi.Input[str] kms_key_arn: The ARN for the KMS encryption key. When specifying `kms_key_arn`, `storage_encrypted` needs to be set to true.
        :param pulumi.Input[str] neptune_cluster_parameter_group_name: A cluster parameter group to associate with the cluster.
        :param pulumi.Input[str] neptune_subnet_group_name: A Neptune subnet group to associate with this Neptune instance.
        :param pulumi.Input[float] port: The port on which the Neptune accepts connections. Default is `8182`.
        :param pulumi.Input[str] preferred_backup_window: The daily time range during which automated backups are created if automated backups are enabled using the BackupRetentionPeriod parameter. Time in UTC. Default: A 30-minute window selected at random from an 8-hour block of time per region. e.g. 04:00-09:00
        :param pulumi.Input[str] preferred_maintenance_window: The weekly time range during which system maintenance can occur, in (UTC) e.g. wed:04:00-wed:04:30
        :param pulumi.Input[str] reader_endpoint: A read-only endpoint for the Neptune cluster, automatically load-balanced across replicas
        :param pulumi.Input[str] replication_source_identifier: ARN of a source Neptune cluster or Neptune instance if this Neptune cluster is to be created as a Read Replica.
        :param pulumi.Input[bool] skip_final_snapshot: Determines whether a final Neptune snapshot is created before the Neptune cluster is deleted. If true is specified, no Neptune snapshot is created. If false is specified, a Neptune snapshot is created before the Neptune cluster is deleted, using the value from `final_snapshot_identifier`. Default is `false`.
        :param pulumi.Input[str] snapshot_identifier: Specifies whether or not to create this cluster from a snapshot. You can use either the name or ARN when specifying a Neptune cluster snapshot, or the ARN when specifying a Neptune snapshot.
        :param pulumi.Input[bool] storage_encrypted: Specifies whether the Neptune cluster is encrypted. The default is `false` if not specified.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the Neptune cluster.
        :param pulumi.Input[list] vpc_security_group_ids: List of VPC security groups to associate with the Cluster

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/neptune_cluster.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["apply_immediately"] = apply_immediately
        __props__["arn"] = arn
        __props__["availability_zones"] = availability_zones
        __props__["backup_retention_period"] = backup_retention_period
        __props__["cluster_identifier"] = cluster_identifier
        __props__["cluster_identifier_prefix"] = cluster_identifier_prefix
        __props__["cluster_members"] = cluster_members
        __props__["cluster_resource_id"] = cluster_resource_id
        __props__["endpoint"] = endpoint
        __props__["engine"] = engine
        __props__["engine_version"] = engine_version
        __props__["final_snapshot_identifier"] = final_snapshot_identifier
        __props__["hosted_zone_id"] = hosted_zone_id
        __props__["iam_database_authentication_enabled"] = iam_database_authentication_enabled
        __props__["iam_roles"] = iam_roles
        __props__["kms_key_arn"] = kms_key_arn
        __props__["neptune_cluster_parameter_group_name"] = neptune_cluster_parameter_group_name
        __props__["neptune_subnet_group_name"] = neptune_subnet_group_name
        __props__["port"] = port
        __props__["preferred_backup_window"] = preferred_backup_window
        __props__["preferred_maintenance_window"] = preferred_maintenance_window
        __props__["reader_endpoint"] = reader_endpoint
        __props__["replication_source_identifier"] = replication_source_identifier
        __props__["skip_final_snapshot"] = skip_final_snapshot
        __props__["snapshot_identifier"] = snapshot_identifier
        __props__["storage_encrypted"] = storage_encrypted
        __props__["tags"] = tags
        __props__["vpc_security_group_ids"] = vpc_security_group_ids
        return Cluster(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

