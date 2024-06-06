from typing import List

from fastapi import APIRouter

from models.transaction_model import SolicitacaoTransacao, TransacaoSimples
from service.service_transacao import TransacaoService

router = APIRouter()


@router.post("", response_model=List[TransacaoSimples], status_code=201)
async def criar_transacoes(transacao: SolicitacaoTransacao) -> List[TransacaoSimples]:
    return await TransacaoService().criar_transacoes(transacao)
