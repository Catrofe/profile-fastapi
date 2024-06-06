from fastapi import APIRouter

from models.transaction_model import TransacaoSimples

router = APIRouter()


@router.post("", response_model=TransacaoSimples, status_code=201)
async def criar_transacoes(transacao: TransacaoSimples) -> TransacaoSimples:
    return {"message": "Transaction created successfully"}
