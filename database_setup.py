import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Categories(Base):
    __tablename__ = 'categories'

    name = Column(String(100), nullable = False)
    id = Column(Integer, primary_key = True)


class Books(Base):
    __tablename__ = 'books'

    name = Column(String(100), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(500))
    user_association = Column(String(100))
    category_id = Column(Integer, ForeignKey('categories.id'), nullable = False)
    categories = relationship(Categories)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
