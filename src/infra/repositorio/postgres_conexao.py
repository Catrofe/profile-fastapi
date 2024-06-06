import logging
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    async_sessionmaker,
    close_all_sessions,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.infra.config import settings


class SingletonMeta(type):
    _instances = None

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Base(AsyncAttrs, DeclarativeBase):  # type: ignore
    pass


class PostgresConexao(metaclass=SingletonMeta):

    def __init__(self):
        self.session_maker: Any = None

    async def gera_conexao(self) -> None:
        """Inicia a conexão com o postgres."""
        if not settings.DB_URL:
            logging.warning(
                "Não foi possível obter a string de conexão com o postgres."
            )
            raise

        engine: AsyncEngine = create_async_engine(
            settings.DB_URL, pool_size=5, max_overflow=0
        )

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        self.session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async def busca_session_maker(self):
        return self.session_maker

    async def fechar_conexao(self) -> None:
        """Fecha a conexão com o postgres."""
        await close_all_sessions()
