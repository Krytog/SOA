from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreatePostRequest(_message.Message):
    __slots__ = ["author_id", "content"]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    author_id: int
    content: str
    def __init__(self, author_id: _Optional[int] = ..., content: _Optional[str] = ...) -> None: ...

class UpdatePostRequest(_message.Message):
    __slots__ = ["user_id", "post_id", "new_content"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_CONTENT_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    post_id: int
    new_content: str
    def __init__(self, user_id: _Optional[int] = ..., post_id: _Optional[int] = ..., new_content: _Optional[str] = ...) -> None: ...

class PostId(_message.Message):
    __slots__ = ["post_id"]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    def __init__(self, post_id: _Optional[int] = ...) -> None: ...

class StatusResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class PostResponse(_message.Message):
    __slots__ = ["post_id", "author_id", "content", "created", "last_modified"]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    LAST_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    author_id: int
    content: str
    created: _timestamp_pb2.Timestamp
    last_modified: _timestamp_pb2.Timestamp
    def __init__(self, post_id: _Optional[int] = ..., author_id: _Optional[int] = ..., content: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_modified: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class PostsListRequest(_message.Message):
    __slots__ = ["user_id", "page_num", "page_size"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_NUM_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    page_num: int
    page_size: int
    def __init__(self, user_id: _Optional[int] = ..., page_num: _Optional[int] = ..., page_size: _Optional[int] = ...) -> None: ...

class PostsListResponse(_message.Message):
    __slots__ = ["posts"]
    POSTS_FIELD_NUMBER: _ClassVar[int]
    posts: _containers.RepeatedCompositeFieldContainer[PostResponse]
    def __init__(self, posts: _Optional[_Iterable[_Union[PostResponse, _Mapping]]] = ...) -> None: ...

class DeletePostRequest(_message.Message):
    __slots__ = ["user_id", "post_id"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    post_id: int
    def __init__(self, user_id: _Optional[int] = ..., post_id: _Optional[int] = ...) -> None: ...
