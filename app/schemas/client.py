from pydantic import BaseModel, EmailStr


class ClientPydant(BaseModel):
    id: int
    email: EmailStr
    password: str
    # refresh_token: str

    class Config:
        orm_mode = True
        from_orm = True
        from_attributes = True
