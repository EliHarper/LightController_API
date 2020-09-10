# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: message.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='message.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rmessage.proto\"\xae\x01\n\rChangeRequest\x12\x0b\n\x03_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06\x63olors\x18\x03 \x03(\t\x12\x19\n\x11\x64\x65\x66\x61ultBrightness\x18\x04 \x01(\x02\x12\x14\n\x0c\x66unctionCall\x18\x05 \x01(\t\x12\x10\n\x08\x61nimated\x18\x06 \x01(\x08\x12\x11\n\tanimation\x18\x07 \x01(\t\x12\r\n\x05index\x18\x08 \x01(\x05\x12\r\n\x05value\x18\t \x01(\t\"\x1b\n\x0btuple_color\x12\x0c\n\x04item\x18\x01 \x03(\x05\"-\n\rColorsRequest\x12\x1c\n\x06\x63olors\x18\x01 \x03(\x0b\x32\x0c.tuple_color\"\x1e\n\x0b\x43hangeReply\x12\x0f\n\x07message\x18\x01 \x01(\t2m\n\x08\x45xecutor\x12-\n\x0b\x41pplyChange\x12\x0e.ChangeRequest\x1a\x0c.ChangeReply\"\x00\x12\x32\n\x0e\x41pplyAmbiLight\x12\x0e.ColorsRequest\x1a\x0c.ChangeReply\"\x00(\x01\x62\x06proto3'
)




_CHANGEREQUEST = _descriptor.Descriptor(
  name='ChangeRequest',
  full_name='ChangeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='_id', full_name='ChangeRequest._id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='ChangeRequest.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='colors', full_name='ChangeRequest.colors', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='defaultBrightness', full_name='ChangeRequest.defaultBrightness', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='functionCall', full_name='ChangeRequest.functionCall', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='animated', full_name='ChangeRequest.animated', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='animation', full_name='ChangeRequest.animation', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='index', full_name='ChangeRequest.index', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='ChangeRequest.value', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=192,
)


_TUPLE_COLOR = _descriptor.Descriptor(
  name='tuple_color',
  full_name='tuple_color',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='item', full_name='tuple_color.item', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=194,
  serialized_end=221,
)


_COLORSREQUEST = _descriptor.Descriptor(
  name='ColorsRequest',
  full_name='ColorsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='colors', full_name='ColorsRequest.colors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=223,
  serialized_end=268,
)


_CHANGEREPLY = _descriptor.Descriptor(
  name='ChangeReply',
  full_name='ChangeReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='ChangeReply.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=270,
  serialized_end=300,
)

_COLORSREQUEST.fields_by_name['colors'].message_type = _TUPLE_COLOR
DESCRIPTOR.message_types_by_name['ChangeRequest'] = _CHANGEREQUEST
DESCRIPTOR.message_types_by_name['tuple_color'] = _TUPLE_COLOR
DESCRIPTOR.message_types_by_name['ColorsRequest'] = _COLORSREQUEST
DESCRIPTOR.message_types_by_name['ChangeReply'] = _CHANGEREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ChangeRequest = _reflection.GeneratedProtocolMessageType('ChangeRequest', (_message.Message,), {
  'DESCRIPTOR' : _CHANGEREQUEST,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:ChangeRequest)
  })
_sym_db.RegisterMessage(ChangeRequest)

tuple_color = _reflection.GeneratedProtocolMessageType('tuple_color', (_message.Message,), {
  'DESCRIPTOR' : _TUPLE_COLOR,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:tuple_color)
  })
_sym_db.RegisterMessage(tuple_color)

ColorsRequest = _reflection.GeneratedProtocolMessageType('ColorsRequest', (_message.Message,), {
  'DESCRIPTOR' : _COLORSREQUEST,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:ColorsRequest)
  })
_sym_db.RegisterMessage(ColorsRequest)

ChangeReply = _reflection.GeneratedProtocolMessageType('ChangeReply', (_message.Message,), {
  'DESCRIPTOR' : _CHANGEREPLY,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:ChangeReply)
  })
_sym_db.RegisterMessage(ChangeReply)



_EXECUTOR = _descriptor.ServiceDescriptor(
  name='Executor',
  full_name='Executor',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=302,
  serialized_end=411,
  methods=[
  _descriptor.MethodDescriptor(
    name='ApplyChange',
    full_name='Executor.ApplyChange',
    index=0,
    containing_service=None,
    input_type=_CHANGEREQUEST,
    output_type=_CHANGEREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ApplyAmbiLight',
    full_name='Executor.ApplyAmbiLight',
    index=1,
    containing_service=None,
    input_type=_COLORSREQUEST,
    output_type=_CHANGEREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_EXECUTOR)

DESCRIPTOR.services_by_name['Executor'] = _EXECUTOR

# @@protoc_insertion_point(module_scope)
