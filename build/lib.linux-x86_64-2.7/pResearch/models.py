from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import pResearch.settings


DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**pResearch.settings.DATABASE))


def create_deals_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Products(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "products"
    id = Column('id', String, primary_key=True)
    date = Column('date', DateTime, nullable=True)
    date_str = Column('date_str', String)
    sub = Column('sub', String)
    name = Column('name', String)
    brand = Column('brand', String)
    price = Column('price', Integer, nullable=True)
    image_link = Column('image_link', String, nullable=True)
    sells = Column('sells', Integer, nullable=True)
    location = Column('location', String, nullable=True)
    product_link = Column('product_link', String, nullable=True)


class HInfo(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "hist_info"
    id = Column(Integer, primary_key=True)
    date = Column('date', DateTime, nullable=True)
    date_str = Column('date_str', String)
    id_product = Column('id_product', String, ForeignKey("products.id"))
    price = Column('price', Integer, nullable=True)
    sells = Column('sells', Integer, nullable=True)