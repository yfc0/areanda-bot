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
    role: Mapped[str] = mapped_column(default="user")

    orders: Mapped[list["Order"]] = relationship()


class Category(Base):
    """Таблица категорий"""

    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    products: Mapped[list["Product"]] = relationship()


class Product(Base):
    """Таблица товара"""

    __tablename__ = "product"
    __table_args__ = (CheckConstraint("status in ('neutral', 'rented')"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    photo: Mapped[str]
    status: Mapped[str] = mapped_column(default="neutral")

    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))


class Order(Base):
    '''Таблица заказа'''

    __tablename__ = "order"
    __table_args__ = (CheckConstraint("type_ in ('rent', 'rent_out')"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    end_rent: Mapped[datetime]
    paid: Mapped[bool | None] = mapped_column(default=False)
    type_: Mapped[str]

    order_items: Mapped[List["OrderItem"]] = relationship(lazy='selectin')
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))


class OrderItem(Base):
    '''Товары для заказа'''

    __tablename__ = "order_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
