import sys
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = True)
    salt = Column(String(250), nullable = False)
    hashedpw = Column(String(250), nullable = False)
    dt_added = Column(DateTime, nullable = False, default = datetime.datetime.now())


class CatalogItem(Base):
    __tablename__ = 'catalog_item'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    price = Column(String(8))
    category = Column(String(250))
    description = Column(String(250))
    dt_added = Column(DateTime, nullable = False, default = datetime.datetime.now())
    dt_modded = Column(DateTime, nullable = False, default = datetime.datetime.now(), onupdate = datetime.datetime.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'category': self.course,
        }


engine = create_engine('sqlite:///catalogitem.db')

Base.metadata.create_all(engine)
