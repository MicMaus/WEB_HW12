from pydantic import BaseModel, PastDate, EmailStr, constr


class UserPydant(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    phone: constr(pattern=r"^\+?[1-9]\d{8,14}$")
    birthday: PastDate
    additional_description: str | None
    # not mandatory field, but 'None' needs to be received from frontend!

    # for proper converting to sql alchem model:
    class Config:
        orm_mode = True
        from_orm = True
        from_attributes = True


class UserUpdatePydant(BaseModel):
    name: str | None
    surname: str | None
    email: EmailStr | None
    phone: constr(pattern=r"^\+?[1-9]\d{8,14}$") | None
    birthday: PastDate | None
    additional_description: str | None
