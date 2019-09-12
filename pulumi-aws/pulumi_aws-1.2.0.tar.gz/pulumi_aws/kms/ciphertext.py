# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Ciphertext(pulumi.CustomResource):
    ciphertext_blob: pulumi.Output[str]
    """
    Base64 encoded ciphertext
    """
    context: pulumi.Output[dict]
    """
    An optional mapping that makes up the encryption context.
    """
    key_id: pulumi.Output[str]
    """
    Globally unique key ID for the customer master key.
    """
    plaintext: pulumi.Output[str]
    """
    Data to be encrypted. Note that this may show up in logs, and it will be stored in the state file.
    """
    def __init__(__self__, resource_name, opts=None, context=None, key_id=None, plaintext=None, __props__=None, __name__=None, __opts__=None):
        """
        The KMS ciphertext resource allows you to encrypt plaintext into ciphertext
        by using an AWS KMS customer master key. The value returned by this resource
        is stable across every apply. For a changing ciphertext value each apply, see
        the [`kms.Ciphertext` data source](https://www.terraform.io/docs/providers/aws/d/kms_ciphertext.html).
        
        > **Note:** All arguments including the plaintext be stored in the raw state as plain-text.
        [Read more about sensitive data in state](https://www.terraform.io/docs/state/sensitive-data.html).
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] context: An optional mapping that makes up the encryption context.
        :param pulumi.Input[str] key_id: Globally unique key ID for the customer master key.
        :param pulumi.Input[str] plaintext: Data to be encrypted. Note that this may show up in logs, and it will be stored in the state file.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/kms_ciphertext.html.markdown.
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

            __props__['context'] = context
            if key_id is None:
                raise TypeError("Missing required property 'key_id'")
            __props__['key_id'] = key_id
            if plaintext is None:
                raise TypeError("Missing required property 'plaintext'")
            __props__['plaintext'] = plaintext
            __props__['ciphertext_blob'] = None
        super(Ciphertext, __self__).__init__(
            'aws:kms/ciphertext:Ciphertext',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, ciphertext_blob=None, context=None, key_id=None, plaintext=None):
        """
        Get an existing Ciphertext resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ciphertext_blob: Base64 encoded ciphertext
        :param pulumi.Input[dict] context: An optional mapping that makes up the encryption context.
        :param pulumi.Input[str] key_id: Globally unique key ID for the customer master key.
        :param pulumi.Input[str] plaintext: Data to be encrypted. Note that this may show up in logs, and it will be stored in the state file.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/kms_ciphertext.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["ciphertext_blob"] = ciphertext_blob
        __props__["context"] = context
        __props__["key_id"] = key_id
        __props__["plaintext"] = plaintext
        return Ciphertext(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

