from pydantic import BaseModel, EmailStr


class ClientPydant(BaseModel):
    id: int
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        from_orm = True
        from_attributes = True


class ClientResponsePydant(BaseModel):
    user: ClientPydant
    detail: str = "Client successfully created"


class TokenPydant(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
