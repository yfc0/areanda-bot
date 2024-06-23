from typing import List, Optional, Annotated
from sqlalchemy import func, ForeignKey, Column, BigInteger, CheckConstraint
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
    __table_args__ = (CheckConstraint("heart >= 0"), CheckConstraint("heart < 4"))
    id: Mapped[int_64] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    heart: Mapped[int] = mapped_column(default=3)
    phone_number: Mapped[str]

class Category(Base):
    """Таблица категорий"""

    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Product(Base):
    """Таблица товара"""

    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    status: Mapped[bool]
