# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protocols.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fprotocols.proto\x12\x17statistics_service_grpc\x1a\x1bgoogle/protobuf/empty.proto\"(\n\x15PostStatisticsRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x04\"G\n\x16PostStatisticsResponse\x12\r\n\x05likes\x18\x01 \x01(\x04\x12\r\n\x05views\x18\x02 \x01(\x04\x12\x0f\n\x07post_id\x18\x03 \x01(\x04\"*\n\x0fTopPostsRequest\x12\x17\n\x0fsorted_by_likes\x18\x01 \x01(\x08\"-\n\x0bTopPostInfo\x12\x0f\n\x07post_id\x18\x01 \x01(\x04\x12\r\n\x05\x63ount\x18\x02 \x01(\x04\"G\n\x10TopPostsResponse\x12\x33\n\x05posts\x18\x01 \x03(\x0b\x32$.statistics_service_grpc.TopPostInfo\"+\n\x0eUserStatistics\x12\n\n\x02id\x18\x01 \x01(\x04\x12\r\n\x05likes\x18\x02 \x01(\x04\"J\n\x10TopUsersResponse\x12\x36\n\x05users\x18\x01 \x03(\x0b\x32\'.statistics_service_grpc.UserStatistics2\xc5\x02\n\x11StatisticsService\x12v\n\x11GetPostStatistics\x12..statistics_service_grpc.PostStatisticsRequest\x1a/.statistics_service_grpc.PostStatisticsResponse\"\x00\x12\x64\n\x0bGetTopPosts\x12(.statistics_service_grpc.TopPostsRequest\x1a).statistics_service_grpc.TopPostsResponse\"\x00\x12R\n\x0bGetTopUsers\x12\x16.google.protobuf.Empty\x1a).statistics_service_grpc.TopUsersResponse\"\x00\x42 Z\x1eproto/;statistics_service_grpcb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protocols_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\036proto/;statistics_service_grpc'
  _globals['_POSTSTATISTICSREQUEST']._serialized_start=73
  _globals['_POSTSTATISTICSREQUEST']._serialized_end=113
  _globals['_POSTSTATISTICSRESPONSE']._serialized_start=115
  _globals['_POSTSTATISTICSRESPONSE']._serialized_end=186
  _globals['_TOPPOSTSREQUEST']._serialized_start=188
  _globals['_TOPPOSTSREQUEST']._serialized_end=230
  _globals['_TOPPOSTINFO']._serialized_start=232
  _globals['_TOPPOSTINFO']._serialized_end=277
  _globals['_TOPPOSTSRESPONSE']._serialized_start=279
  _globals['_TOPPOSTSRESPONSE']._serialized_end=350
  _globals['_USERSTATISTICS']._serialized_start=352
  _globals['_USERSTATISTICS']._serialized_end=395
  _globals['_TOPUSERSRESPONSE']._serialized_start=397
  _globals['_TOPUSERSRESPONSE']._serialized_end=471
  _globals['_STATISTICSSERVICE']._serialized_start=474
  _globals['_STATISTICSSERVICE']._serialized_end=799
# @@protoc_insertion_point(module_scope)
