from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PostStatisticsRequest(_message.Message):
    __slots__ = ["post_id"]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    def __init__(self, post_id: _Optional[int] = ...) -> None: ...

class PostStatisticsResponse(_message.Message):
    __slots__ = ["likes", "views", "post_id"]
    LIKES_FIELD_NUMBER: _ClassVar[int]
    VIEWS_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    likes: int
    views: int
    post_id: int
    def __init__(self, likes: _Optional[int] = ..., views: _Optional[int] = ..., post_id: _Optional[int] = ...) -> None: ...

class PostWithAuthorStatistics(_message.Message):
    __slots__ = ["post_id", "author_id", "likes", "views"]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    LIKES_FIELD_NUMBER: _ClassVar[int]
    VIEWS_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    author_id: int
    likes: int
    views: int
    def __init__(self, post_id: _Optional[int] = ..., author_id: _Optional[int] = ..., likes: _Optional[int] = ..., views: _Optional[int] = ...) -> None: ...

class TopPostsRequest(_message.Message):
    __slots__ = ["sorted_by_likes"]
    SORTED_BY_LIKES_FIELD_NUMBER: _ClassVar[int]
    sorted_by_likes: bool
    def __init__(self, sorted_by_likes: bool = ...) -> None: ...

class TopPostsResponse(_message.Message):
    __slots__ = ["posts"]
    POSTS_FIELD_NUMBER: _ClassVar[int]
    posts: _containers.RepeatedCompositeFieldContainer[PostWithAuthorStatistics]
    def __init__(self, posts: _Optional[_Iterable[_Union[PostWithAuthorStatistics, _Mapping]]] = ...) -> None: ...

class UserStatistics(_message.Message):
    __slots__ = ["id", "likes"]
    ID_FIELD_NUMBER: _ClassVar[int]
    LIKES_FIELD_NUMBER: _ClassVar[int]
    id: int
    likes: int
    def __init__(self, id: _Optional[int] = ..., likes: _Optional[int] = ...) -> None: ...

class TopUsersResponse(_message.Message):
    __slots__ = ["users"]
    USERS_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[UserStatistics]
    def __init__(self, users: _Optional[_Iterable[_Union[UserStatistics, _Mapping]]] = ...) -> None: ...
