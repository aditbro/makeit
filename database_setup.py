import os
import sys
import flask_login
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.hash import bcrypt

Base = declarative_base()

class User(Base,flask_login.UserMixin):
	__tablename__ = 'user'
	username = Column(String(160), nullable=False, unique=True, primary_key=True)
	password = Column(String(160), nullable=False)
	name = Column(String(255), nullable=False)
	email = Column(String(255), nullable=False)
	gender = Column(String(6), nullable=False)
	birth_date = Column(String(10), nullable=False)
	phone_number = Column(String(50), nullable=False)
	address = Column(String(255), nullable=False)
	photodir = Column(String(1000))
	verified = Column(Integer, nullable=False)

	def __init__(self, username, password, name, email, gender, birth_date, phone_number, address, photodir):
		self.username = username
		self.password = bcrypt.encrypt(password)
		self.name = name
		self.email = email
		self.gender = gender
		self.birth_date = birth_date
		self.phone_number = phone_number
		self.address = address
		self.photodir = photodir
		self.verified = 0

	def verify_password(self, password):
		return bcrypt.verify(password,self.password)


class Shop(Base):
	__tablename__ = 'shop'
	id = Column(Integer, primary_key=True)
	name = Column(String(160), nullable=False, unique=True)
	user = Column(String(160), ForeignKey('user.username'), nullable=False)

class Article(Base):
	__tablename__ = 'article'
	id = Column(Integer, primary_key=True)
	title = Column(String(100), nullable=False, unique=True)
	content = Column(String(4000), nullable=False)
	date_created = Column(String(10), nullable=False)
	shop = Column(String(160), ForeignKey('shop.name'), nullable=False)

class ShopPhoto(Base):
	__tablename__ = 'shopphoto'
	shopname = Column(String(160), ForeignKey('shop.name'))
	dir = Column(String(1000), primary_key=True)

class ArticlePhoto(Base):
	__tablename__ = 'articlephoto'
	articlename = Column(String(100), ForeignKey('article.title'))
	dir = dir = Column(String(1000), primary_key=True)

class ShopTag(Base):
	__tablename__ = 'shoptag'
	name = Column(String(160), ForeignKey('shop.name'), primary_key=True)
	tag = Column(String(160), ForeignKey('tags.name'), primary_key=True)

class Tags(Base):
	__tablename__ = 'tags'
	name = Column(String(160), primary_key=True)

engine = create_engine('sqlite:///main.db')


Base.metadata.create_all(engine)
