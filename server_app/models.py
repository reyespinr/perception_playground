from enum import Enum
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserRole(Enum):
    ADMIN = "admin"
    REGULAR = "viewer"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(150), nullable=False)
    role = Column(String(80), nullable=False)
