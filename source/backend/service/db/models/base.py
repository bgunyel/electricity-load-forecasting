import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base

Base: Engine = declarative_base()


class ObjectTimestamps(Base):
    __abstract__ = True

    created_at = Column(
        "created_at", DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )
    updated_at = Column(
        "updated_at", DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )


class ObjectBase(ObjectTimestamps):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
