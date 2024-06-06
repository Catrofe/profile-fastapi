from sqlalchemy import DECIMAL, Column, DateTime, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):  # type: ignore
    pass


class Transacao(Base):
    __tablename__ = "transacao"

    id = Column(Integer, primary_key=True, index=True)
    ativo = Column(String, nullable=False)
    valor = Column(DECIMAL, nullable=False)
    data = Column(DateTime, nullable=False)
