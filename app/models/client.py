from sqlalchemy import Column, String
from .base import BaseModel, Base


class ClientDB(BaseModel):
    __tablename__ = "clients_table"
    email = Column(String, unique=True)
    password = Column(String)
    refresh_token = Column(String)
