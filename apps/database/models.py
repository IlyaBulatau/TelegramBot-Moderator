from sqlalchemy import String, BigInteger, Integer, Column, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__='users'

    tg_id = Column(BigInteger(), primary_key=True, unique=True)
    warning_count = Column(Integer(), nullable=False, default=0)