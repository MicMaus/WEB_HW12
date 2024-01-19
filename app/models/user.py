from sqlalchemy import Column, Integer, String, DateTime
from .base import BaseModel, Base


class UserDB(BaseModel):
    __tablename__ = "users_table"
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    phone = Column(String)
    birthday = Column(DateTime)
    additional_description = Column(String)
