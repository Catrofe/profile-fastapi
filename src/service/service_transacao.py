import asyncio
import random
from typing import List

from infra.repositorio.entity import Transacao
from models.transaction_model import (
    SolicitacaoTransacao,
    TransacaoRegistrada,
    TransacaoSimples,
)
from repository.repositorio_transacao import TransacaoRepositorio


class TransacaoService:
    def __init__(self) -> None:
        self._repositorio = TransacaoRepositorio()

    async def criar_transacoes(
        self, transacao: SolicitacaoTransacao
    ) -> List[TransacaoRegistrada]:
        tarefas = [
            self.criar_transacao_individual(
                transacao.ativos[random.randint(0, len(transacao.ativos) - 1)]
            )
            for _ in range(transacao.quantidadeAtivos)
        ]
        transacoes = await asyncio.gather(*tarefas)
        transacoes_registradas = await self._repositorio.registrar_transacoes(
            transacoes
        )
        return [
            await self.parsea_entity_para_model(transacao)
            for transacao in transacoes_registradas
        ]

    async def criar_transacao_individual(self, ativo: str) -> TransacaoSimples:
        return TransacaoSimples(ativo=ativo, valor=random.uniform(1.0, 100.0))

    async def parsea_entity_para_model(
        self, transacao: Transacao
    ) -> TransacaoRegistrada:
        return TransacaoRegistrada(
            id=transacao.id,
            ativo=transacao.ativo,
            valor=transacao.valor,
            data=transacao.data,
        )
