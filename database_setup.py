#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os  # For heroku deploy
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from passlib.apps import custom_app_context as pwd_context


DB_CONFIG_DICT = {
    'user': '<YOUR USERNAME>',
    'password': '<YOUR PASSWORD>',
    'host': 'localhost',
    'port': 5432,
    'database': 'catalog'
    }

# For own use, change the DB Connection format to the following
# DB_CONN_FORMAT = "postgresql://{user}:{password}@{host}:{port}/{database}"
# DB_CONN_FORMAT = "postgresql:///{database}"
# DB_CONN_URI = DB_CONN_FORMAT.format(**DB_CONFIG_DICT)
DB_CONN_URI = os.environ['DATABASE_URL']

Base = declarative_base()


class user_with_item(Base):
    __tablename__ = "user_with_item"

    uid = Column(Integer, ForeignKey('users.id'), primary_key=True)
    iid = Column(Integer, ForeignKey('items.id'), primary_key=True)
    lastEditTime = Column(DateTime, server_default=func.now(),
                          onupdate=func.now())
    user = relationship('User', back_populates='items')
    item = relationship('Item', back_populates='users')


class category_with_item(Base):
    __tablename__ = "category_with_item"

    cid = Column(Integer, ForeignKey('categories.id'), primary_key=True)
    iid = Column(Integer, ForeignKey('items.id'), primary_key=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, index=True, nullable=False, unique=True)
    username = Column(String, nullable=False)
    password = Column(String(128))
    photo = Column(String)
    items = relationship('user_with_item', order_by='user_with_item.iid',
                         cascade="all, delete, delete-orphan",
                         back_populates='user')

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def validate_password(self, password):
        return pwd_context.verify(password, self.password)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False, index=True)
    items = relationship('Item', order_by='Item.id',
                         secondary=category_with_item.__table__,
                         back_populates='categories')

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
    categories = relationship('Category', back_populates='items',
                              secondary=category_with_item.__table__)
    users = relationship('user_with_item',
                         back_populates='item')
    refers = relationship('Reference', back_populates='items')

    @property
    def serialize(self):
        """ Return object datatype that is easily serializable """
        return {
                'item': self.name,
                'description': self.description,
                'references': [r.serialize for r in self.refers],
                'category': [c.name for c in self.categories],
                'lastEditTime': self.lastEditTime.strftime("%Y-%m-%d %H:%M"),
                'lastEditedBy': self.findLastEditUser()
        }

    def findLastEditUser(self):
        return max([(u.lastEditTime, u.user.username) for u in self.users])[1]


class Reference(Base):
    __tablename__ = 'references'

    id = Column(Integer, primary_key=True, autoincrement=True)
    iid = Column(Integer, ForeignKey('items.id'), primary_key=True)
    rlink = Column(String)
    rtext = Column(String)
    items = relationship('Item', back_populates='refers')

    @property
    def serialize(self):
        """ Return object that is easily serializable """
        return {
                'references': self.rtext + '[' + self.rlink + ']'
        }


if __name__ == "__main__":
    engine = create_engine(DB_CONN_URI, echo=False)
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)
