from __future__ import annotations

from sqlalchemy import TIMESTAMP, text, Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped

Base = declarative_base()


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    type = Column(String(100))
    description = Column(Text())
    create_date = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_date = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))


class UserInDB(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(100), unique=True)
    email = Column(String(100), unique=True)
    disabled = Column(Boolean, default=True)
    hashed_password = Column(String(255))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    role_id = Column(Integer, ForeignKey("role.id"))

    # role: Mapped["Role"] = relationship("Role", back_populates="users")


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_name = Column(String(255))

    # users: Mapped["User"] = relationship("User")

