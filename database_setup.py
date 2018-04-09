#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


DB_CONFIG_DICT = {
    'user': '<YOUR USERNAME>',
    'password': '<YOUR PASSWORD>',
    'host': 'localhost',
    'port': 5432,
    'database': 'catalog'
    }

# For own use, change the DB Connection format to the following
# DB_CONN_FORMAT = "postgresql://{user}:{password}@{host}:{port}/{database}"
DB_CONN_FORMAT = "postgresql:///{database}"
DB_CONN_URI = DB_CONN_FORMAT.format(**DB_CONFIG_DICT)


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, index=True, nullable=False, unique=True)
    username = Column(String, nullable=False)
    password = Column(String(512), nullable=False)
    items = relationship('Item', order_by='Item.id',
                         cascade="all, delete, delete-orphan",
                         back_populates='user')

    @staticmethod
    def validate_password(self):
        pass


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False, index=True)
    items = relationship('Item', order_by='Item.id',
                         cascade="all, delete, delete-orphan",
                         back_populates='category')

    @property
    def serialize(self):
        """ Return object datatype that is easily serializable"""
        return {
                'category': self.name,
                'items': [item.serialize for item in self.items]
        }


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String)
    imageURI = Column(String)
    lastEditTime = Column(DateTime, server_default=func.now(),
                          onupdate=func.now())
    cid = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Category, back_populates='items')
    uid = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, back_populates="items")

    @property
    def serialize(self):
        """ Return object datatype that is easily serializable """
        return {
                'item': self.name,
                'description': ' '.join(self.description.split()),
                'category': self.category.name,
                'lastEditTime': self.lastEditTime
        }


engine = create_engine(DB_CONN_URI, echo=False)
if not database_exists(engine.url):
    create_database(engine.url)
Base.metadata.create_all(engine)
