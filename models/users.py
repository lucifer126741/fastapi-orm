from sqlalchemy import Column, Integer, String

from config.db import Base


class User(Base):
    __tablename__ = 'fastapi-users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False, unique=True)
