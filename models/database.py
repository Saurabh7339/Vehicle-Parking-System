from datetime import datetime
from sqlalchemy import DateTime, create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlmodel import SQLModel, Field

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DB_PATH = "/home/dante/Desktop/fastapi_sample/sql_fastapi_db/db.db"


print(BASE_DIR,DB_PATH)

DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False})

metadata = MetaData()

Base = declarative_base(metadata=metadata)
def init_db():
    SQLModel.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# with engine.connect() as connection:
#     connection.execute('PRAGMA journal_mode=WAL;')
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    __tablename__ = "user"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True) 
    age = Column(Integer, primary_key=False, index=True)


class Parking(SQLModel, table=True):
    __tablename__ = "parking"
    __allow_unmapped__ = True
    # id = Column(Integer, primary_key=True, index=True)
    # vehicle_number = Column(String, index=True)
    # name = Column(String, unique=False, index=True) 
    # time_in =  Column(DateTime, default=datetime.utcnow)
    # time_out = Column(DateTime, nullable=True)
    # parking_type = Column(String, unique=True, index=True)

    id: int = Field(default=None, primary_key=True, index=True)
    vehicle_number: str = Field(default=None, index=True)
    name: str = Field(default=None, index=True)
    time_in: datetime = Field(default_factory=datetime.utcnow)
    time_out:  datetime | None = Field(default=None, nullable=True) 
    parking_type: str |None  = None
