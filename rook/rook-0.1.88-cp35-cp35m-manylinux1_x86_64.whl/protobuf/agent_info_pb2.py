# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: agent_info.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='agent_info.proto',
  package='com.rookout',
  syntax='proto3',
  serialized_pb=_b('\n\x10\x61gent_info.proto\x12\x0b\x63om.rookout\"0\n\x0eSCMInformation\x12\x0e\n\x06\x63ommit\x18\x01 \x01(\t\x12\x0e\n\x06origin\x18\x02 \x01(\t\"K\n\x12NetworkInformation\x12\x0f\n\x07ip_addr\x18\x01 \x01(\t\x12\x0f\n\x07network\x18\x02 \x01(\t\x12\x13\n\x0b\x65xternal_ip\x18\x03 \x01(\t\"c\n\x11SystemInformation\x12\x10\n\x08hostname\x18\x01 \x01(\t\x12\n\n\x02os\x18\x02 \x01(\t\x12\x12\n\nos_version\x18\x03 \x01(\t\x12\x0e\n\x06\x64istro\x18\x04 \x01(\t\x12\x0c\n\x04\x61rch\x18\x05 \x01(\t\"5\n\x12VersionInformation\x12\x0f\n\x07version\x18\x01 \x01(\t\x12\x0e\n\x06\x63ommit\x18\x02 \x01(\t\"I\n\x13PlatformInformation\x12\x10\n\x08platform\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\x0f\n\x07variant\x18\x03 \x01(\t\"\xd1\x03\n\x10\x41gentInformation\x12\x10\n\x08\x61gent_id\x18\x01 \x01(\t\x12\x30\n\x07version\x18\x02 \x01(\x0b\x32\x1f.com.rookout.VersionInformation\x12\x30\n\x07network\x18\x03 \x01(\x0b\x32\x1f.com.rookout.NetworkInformation\x12.\n\x06system\x18\x04 \x01(\x0b\x32\x1e.com.rookout.SystemInformation\x12\x32\n\x08platform\x18\x05 \x01(\x0b\x32 .com.rookout.PlatformInformation\x12\x12\n\nexecutable\x18\x06 \x01(\t\x12\x19\n\x11\x63ommand_arguments\x18\x07 \x03(\t\x12\x12\n\nprocess_id\x18\x08 \x01(\r\x12\x39\n\x06labels\x18\t \x03(\x0b\x32).com.rookout.AgentInformation.LabelsEntry\x12(\n\x03scm\x18\n \x01(\x0b\x32\x1b.com.rookout.SCMInformation\x12\x0c\n\x04tags\x18\x0b \x03(\t\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x62\x06proto3')
)




_SCMINFORMATION = _descriptor.Descriptor(
  name='SCMInformation',
  full_name='com.rookout.SCMInformation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='commit', full_name='com.rookout.SCMInformation.commit', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='origin', full_name='com.rookout.SCMInformation.origin', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=33,
  serialized_end=81,
)


_NETWORKINFORMATION = _descriptor.Descriptor(
  name='NetworkInformation',
  full_name='com.rookout.NetworkInformation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip_addr', full_name='com.rookout.NetworkInformation.ip_addr', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='network', full_name='com.rookout.NetworkInformation.network', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='external_ip', full_name='com.rookout.NetworkInformation.external_ip', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=83,
  serialized_end=158,
)


_SYSTEMINFORMATION = _descriptor.Descriptor(
  name='SystemInformation',
  full_name='com.rookout.SystemInformation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='hostname', full_name='com.rookout.SystemInformation.hostname', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='os', full_name='com.rookout.SystemInformation.os', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='os_version', full_name='com.rookout.SystemInformation.os_version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='distro', full_name='com.rookout.SystemInformation.distro', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='arch', full_name='com.rookout.SystemInformation.arch', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=160,
  serialized_end=259,
)


_VERSIONINFORMATION = _descriptor.Descriptor(
  name='VersionInformation',
  full_name='com.rookout.VersionInformation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='com.rookout.VersionInformation.version', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='commit', full_name='com.rookout.VersionInformation.commit', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=261,
  serialized_end=314,
)


_PLATFORMINFORMATION = _descriptor.Descriptor(
  name='PlatformInformation',
  full_name='com.rookout.PlatformInformation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='platform', full_name='com.rookout.PlatformInformation.platform', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='com.rookout.PlatformInformation.version', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='variant', full_name='com.rookout.PlatformInformation.variant', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=316,
  serialized_end=389,
)


_AGENTINFORMATION_LABELSENTRY = _descriptor.Descriptor(
  name='LabelsEntry',
  full_name='com.rookout.AgentInformation.LabelsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='com.rookout.AgentInformation.LabelsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='com.rookout.AgentInformation.LabelsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=812,
  serialized_end=857,
)

_AGENTINFORMATION = _descriptor.Descriptor(
  name='AgentInformation',
  full_name='com.rookout.AgentInformation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='agent_id', full_name='com.rookout.AgentInformation.agent_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='com.rookout.AgentInformation.version', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='network', full_name='com.rookout.AgentInformation.network', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='system', full_name='com.rookout.AgentInformation.system', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='platform', full_name='com.rookout.AgentInformation.platform', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='executable', full_name='com.rookout.AgentInformation.executable', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='command_arguments', full_name='com.rookout.AgentInformation.command_arguments', index=6,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='process_id', full_name='com.rookout.AgentInformation.process_id', index=7,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='labels', full_name='com.rookout.AgentInformation.labels', index=8,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='scm', full_name='com.rookout.AgentInformation.scm', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='tags', full_name='com.rookout.AgentInformation.tags', index=10,
      number=11, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_AGENTINFORMATION_LABELSENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=392,
  serialized_end=857,
)

_AGENTINFORMATION_LABELSENTRY.containing_type = _AGENTINFORMATION
_AGENTINFORMATION.fields_by_name['version'].message_type = _VERSIONINFORMATION
_AGENTINFORMATION.fields_by_name['network'].message_type = _NETWORKINFORMATION
_AGENTINFORMATION.fields_by_name['system'].message_type = _SYSTEMINFORMATION
_AGENTINFORMATION.fields_by_name['platform'].message_type = _PLATFORMINFORMATION
_AGENTINFORMATION.fields_by_name['labels'].message_type = _AGENTINFORMATION_LABELSENTRY
_AGENTINFORMATION.fields_by_name['scm'].message_type = _SCMINFORMATION
DESCRIPTOR.message_types_by_name['SCMInformation'] = _SCMINFORMATION
DESCRIPTOR.message_types_by_name['NetworkInformation'] = _NETWORKINFORMATION
DESCRIPTOR.message_types_by_name['SystemInformation'] = _SYSTEMINFORMATION
DESCRIPTOR.message_types_by_name['VersionInformation'] = _VERSIONINFORMATION
DESCRIPTOR.message_types_by_name['PlatformInformation'] = _PLATFORMINFORMATION
DESCRIPTOR.message_types_by_name['AgentInformation'] = _AGENTINFORMATION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SCMInformation = _reflection.GeneratedProtocolMessageType('SCMInformation', (_message.Message,), dict(
  DESCRIPTOR = _SCMINFORMATION,
  __module__ = 'agent_info_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.SCMInformation)
  ))
_sym_db.RegisterMessage(SCMInformation)

NetworkInformation = _reflection.GeneratedProtocolMessageType('NetworkInformation', (_message.Message,), dict(
  DESCRIPTOR = _NETWORKINFORMATION,
  __module__ = 'agent_info_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.NetworkInformation)
  ))
_sym_db.RegisterMessage(NetworkInformation)

SystemInformation = _reflection.GeneratedProtocolMessageType('SystemInformation', (_message.Message,), dict(
  DESCRIPTOR = _SYSTEMINFORMATION,
  __module__ = 'agent_info_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.SystemInformation)
  ))
_sym_db.RegisterMessage(SystemInformation)

VersionInformation = _reflection.GeneratedProtocolMessageType('VersionInformation', (_message.Message,), dict(
  DESCRIPTOR = _VERSIONINFORMATION,
  __module__ = 'agent_info_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.VersionInformation)
  ))
_sym_db.RegisterMessage(VersionInformation)

PlatformInformation = _reflection.GeneratedProtocolMessageType('PlatformInformation', (_message.Message,), dict(
  DESCRIPTOR = _PLATFORMINFORMATION,
  __module__ = 'agent_info_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.PlatformInformation)
  ))
_sym_db.RegisterMessage(PlatformInformation)

AgentInformation = _reflection.GeneratedProtocolMessageType('AgentInformation', (_message.Message,), dict(

  LabelsEntry = _reflection.GeneratedProtocolMessageType('LabelsEntry', (_message.Message,), dict(
    DESCRIPTOR = _AGENTINFORMATION_LABELSENTRY,
    __module__ = 'agent_info_pb2'
    # @@protoc_insertion_point(class_scope:com.rookout.AgentInformation.LabelsEntry)
    ))
  ,
  DESCRIPTOR = _AGENTINFORMATION,
  __module__ = 'agent_info_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.AgentInformation)
  ))
_sym_db.RegisterMessage(AgentInformation)
_sym_db.RegisterMessage(AgentInformation.LabelsEntry)


_AGENTINFORMATION_LABELSENTRY.has_options = True
_AGENTINFORMATION_LABELSENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
# @@protoc_insertion_point(module_scope)
