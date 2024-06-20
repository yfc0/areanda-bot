from typing import List, Optional, Annotated
from sqlalchemy import func, ForeignKey, Column, BigInteger
from sqlalchemy.orm import (
    DeclarativeBase,
    registry,
    Mapped,
    mapped_column,
    relationship,
    remote,
    foreign,
)
from datetime import datetime


int_64 = Annotated[BigInteger, "int_64"]

class Base(DeclarativeBase):
    registry = registry(type_annotation_map={int_64: BigInteger()})


class User(Base):
    """Таблица юзера"""

    __tablename__ = "user"
    id: Mapped[int_64] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
