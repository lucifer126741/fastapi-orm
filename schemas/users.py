from typing import Optional
from pydantic import BaseModel


class UserModel(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None

    class Config:
        from_attributes = True

