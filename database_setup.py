import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    """ This class defines the User that will be logged in
        it has the following properties
        id : Integer
        name : String
        email : String
        picture : String of URL 
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Category(Base):
    """ Category class has following properties
        id : Integer
        name : String
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    # Here we return the DB entry as JSON
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class CategoryItem(Base):
    """ Each category has items that belong to it.
        These items have the following properties
        id : Integer
        name : String
        description : String
        category_id : Integer - foreign key 
        category : relationship with the Category Class
    """
    __tablename__ = 'category_item'

    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(500), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)


    # Here we return the DB entry as JSON
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id
        }


# This next line creates a dialect object tailored towards sqlite
# as well as a pool object which will establish a DBAPI connection at
# cataloglist.db

engine = create_engine('sqlite:///cataloglist.db')

# The Connection itself to DBAPI is established in the following line
# For more information refer to 
# http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html
Base.metadata.create_all(engine)

