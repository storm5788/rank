

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative

from sqlalchemy import Column, Integer, String, DateTime, Binary, ForeignKey, Float, BigInteger

from sqlalchemy.ext.declarative import declarative_base


Base=declarative_base()

class user_ranking(Base):
    __tablename__="user_ranking"
    id = Column(Integer, primary_key=True)
    client_code=Column(Integer,unique=True)
    score=Column(Integer)
    rank=Column(Integer,nullable=True)


    def __repr__(self):
        return '<Group id=%d,name=%s>' % (self.id, self.client_code)


