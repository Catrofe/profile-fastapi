from typing import List

from infra.repositorio.entity import Transacao
from infra.repositorio.postgres_conexao import PostgresConexao
from models.transaction_model import TransacaoSimples


class TransacaoRepositorio:
    def __init__(self) -> None:
        self.conexao = PostgresConexao()

    async def registrar_transacoes(
        self, transacoes: List[TransacaoSimples]
    ) -> List[Transacao]:
        transacoes_parseadas: List[Transacao] = [
            await self.parsea_para_entidade(transacao) for transacao in transacoes
        ]
        session_maker = await self.conexao.busca_session_maker()
        async with session_maker() as session:
            async with session.begin():
                session.add_all(transacoes_parseadas)
                await session.commit()

        return transacoes_parseadas

    async def parsea_para_entidade(self, transacao: TransacaoSimples) -> Transacao:
        return Transacao(
            ativo=transacao.ativo, valor=transacao.valor, data=transacao.data
        )
