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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nmain.proto\x12\x06mainpb\"\xf8\x02\n\x08UserData\x12\x13\n\x06status\x18\x01 \x01(\x08H\x00\x88\x01\x01\x12\x11\n\x04info\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x11\n\tfirstName\x18\x03 \x01(\t\x12\x10\n\x08lastName\x18\x04 \x01(\t\x12\x17\n\nmiddleName\x18\x05 \x01(\tH\x02\x88\x01\x01\x12\r\n\x05\x65mail\x18\x06 \x01(\t\x12\x0e\n\x06rating\x18\x07 \x01(\r\x12\x0c\n\x04role\x18\x08 \x01(\r\x12\x19\n\x0ctelegramLink\x18\t \x01(\tH\x03\x88\x01\x01\x12\x17\n\ngithubLink\x18\n \x01(\tH\x04\x88\x01\x01\x12\x17\n\nstepikLink\x18\x0b \x01(\tH\x05\x88\x01\x01\x12\x17\n\nkaggleLink\x18\x0c \x01(\tH\x06\x88\x01\x01\x12\x12\n\navatarPath\x18\r \x01(\tB\t\n\x07_statusB\x07\n\x05_infoB\r\n\x0b_middleNameB\x0f\n\r_telegramLinkB\r\n\x0b_githubLinkB\r\n\x0b_stepikLinkB\r\n\x0b_kaggleLink\"+\n\x08\x41uthData\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"5\n\x0b\x41\x63\x63\x65ssToken\x12\x13\n\x0b\x61\x63\x63\x65ssToken\x18\x01 \x01(\t\x12\x11\n\ttokenType\x18\x02 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'main_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USERDATA._serialized_start=23
  _USERDATA._serialized_end=399
  _AUTHDATA._serialized_start=401
  _AUTHDATA._serialized_end=444
  _ACCESSTOKEN._serialized_start=446
  _ACCESSTOKEN._serialized_end=499
# @@protoc_insertion_point(module_scope)
