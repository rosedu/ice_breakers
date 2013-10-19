__author__ = 'Radu'

from sqlalchemy import create_engine, Column
from sqlalchemy import (Integer, Unicode, String)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

engine = create_engine("mysql+mysqldb://root:password@fbhack.sniffio.com') ")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __repr(self):
        return self.id