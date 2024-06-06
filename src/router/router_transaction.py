from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def criar_transacoes():
    return {"message": "Transaction created successfully"}
