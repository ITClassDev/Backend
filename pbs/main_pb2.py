# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: main.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nmain.proto\x12\x06mainpb\"~\n\x08UserData\x12\x12\n\nfirst_name\x18\x01 \x01(\t\x12\x11\n\tlast_name\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12\r\n\x05\x63oins\x18\x04 \x01(\x03\x12\x0e\n\x06rating\x18\x05 \x01(\x03\x12\x0c\n\x04role\x18\x06 \x01(\x03\x12\x0f\n\x07user_id\x18\x07 \x01(\x03\"+\n\x08\x41uthData\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"7\n\x0b\x41\x63\x63\x65ssToken\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x12\n\ntoken_type\x18\x02 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'main_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USERDATA._serialized_start=22
  _USERDATA._serialized_end=148
  _AUTHDATA._serialized_start=150
  _AUTHDATA._serialized_end=193
  _ACCESSTOKEN._serialized_start=195
  _ACCESSTOKEN._serialized_end=250
# @@protoc_insertion_point(module_scope)
