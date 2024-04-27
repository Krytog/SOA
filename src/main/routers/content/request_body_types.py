from pydantic import BaseModel

class PostContent(BaseModel):
    content: str


class PostsList(BaseModel):
    user_id: int
    page: int
    per_page: int
