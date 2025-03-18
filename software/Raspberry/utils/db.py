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

    macs = relationship("Mac", backref="user")

    def __repr__(self):
        return f"User  (name='{self.name}', tribe='{self.tribe}')"


class Mac(Base):
    __tablename__ = 'macs'

    id = Column(String, primary_key=True)
    led_id = Column(Integer)
    cluster = Column(String)
    user_name = Column(String, ForeignKey('users.name'), nullable=True)

    def __repr__(self):
        return f"Mac  (id='{self.id}', cluster='{self.cluster}', user_name='{self.user_name}')"



class ClusterDB:
    def __init__(self):
        self.engine = create_engine(config('DATABASE_URL'), echo=True)
        Base.metadata.create_all(self.engine)
        self.fill_clusters()

    def create_session(self):
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=self.engine)
        return Session()
    

    def fill_clusters(self):
        session = self.create_session()

        for cluster, mac_ids in Clusters.items():
            for mac_id, count in mac_ids:
                for i in range(1, count + 1):
                    mac = Mac(
                        id=f"{mac_id}{i}",
                        led_id=i-1,
                        cluster=cluster
                    )
                    session.add(mac)
        
        session.commit()
        session.close()

    
    