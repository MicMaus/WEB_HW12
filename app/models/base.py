from dependencies.db import Base
from sqlalchemy import Column, Integer, String, DateTime


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
