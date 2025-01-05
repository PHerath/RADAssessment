from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from config.config import MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB_NAME, ADMIN_USER_PWD, \
    DEFAULT_ADMIN_USER, DEFAULT_ADMIN_EMAIL
from db import models
from util.util import get_password_hash

DATABASE_URL = f'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB_NAME}'

engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,
    pool_size=10,
    pool_pre_ping=True,
    pool_timeout=60,
    echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_db_and_tables():
    models.Base.metadata.create_all(engine)
    # Add default role if it doesn't exist
    with SessionLocal() as session:
        # Check if role already exists
        default_role = session.query(models.Role).filter_by(role_name='admin').first()
        if not default_role:
            default_role = models.Role(role_name='admin')
            session.add(default_role)
            session.commit()

        # Check if user already exists
        default_user = session.query(models.UserInDB).filter_by(user_name='admin').first()
        if not default_user:
            hashed_pwd = get_password_hash(ADMIN_USER_PWD)
            new_user = models.UserInDB(
                user_name=DEFAULT_ADMIN_USER,
                email=DEFAULT_ADMIN_EMAIL,
                hashed_password=hashed_pwd,
                role_id=default_role.id
            )
            session.add(new_user)
            session.commit()


def get_session():
    with SessionLocal() as session:
        yield session


db_dependency = Annotated[Session, Depends(get_session)]


def get_db_session():
    db = next(get_session())
    return db
