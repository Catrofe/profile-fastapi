from sqlalchemy import DECIMAL, Column, DateTime, Integer, String

from src.infra.repositorio.postgres_conexao import Base


class Transacao(Base):

    id = Column(Integer, primary_key=True, index=True)
    ativo = Column(String, nullable=False)
    valor = Column(DECIMAL, nullable=False)
    data = Column(DateTime, nullable=False)
