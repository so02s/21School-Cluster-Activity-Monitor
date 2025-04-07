from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

from decouple import config

from utils.settings import Clusters

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    name = Column(String, primary_key=True)
    tribe = Column(String)

    def __repr__(self):
        return f"User  (name='{self.name}', tribe='{self.tribe}')"

class Mac(Base):
    __tablename__ = 'macs'
    
    login = Column(String, primary_key=True)
    cluster_name = Column(String)
    row = Column(String)
    column = Column(Integer)

    def __init__(self, cluster_name, login, row, column):
        self.login = login
        self.cluster_name = cluster_name
        self.row = row
        self.column = column

