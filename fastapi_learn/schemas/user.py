from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    description: str
    account: str
    password: str
