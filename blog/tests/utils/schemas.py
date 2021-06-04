from pydantic import BaseModel
from typing import Optional


class BlogFaker(BaseModel):
    title: Optional[str]
    body: Optional[str]
