from pydantic import BaseModel
from typing import Optional

class UserModel(BaseModel):
    id: int
    username: Optional[str]
    full_name: Optional[str]







