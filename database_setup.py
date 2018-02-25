import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class RentList(Base):
    __tablename__ = 'rent_list'

    id = Column(Integer, primary_key=True)
    nama = Column(String(80), nullable=False)
    nim = Column(String(8))
    lapangan = Column(String(1), nullable=False)
    tanggal = Column(String(10), nullable=False)
    jam = Column(String(5), nullable=False)
    id_line = Column(String(255), nullable=False)
    meja = Column(Integer, nullable=False)
    net = Column(Integer, nullable=False)
    bet = Column(Integer, nullable=False)
    bola1 = Column(Integer, nullable=False)
    bola3 = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    lama = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)

engine = create_engine('sqlite:///tabletennis.db')


Base.metadata.create_all(engine)
