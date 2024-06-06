from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from utils.models_utils import obter_data_atual


class TransacaoSimples(BaseModel):
    ativo: str = Field(..., title="Ativo", description="Ativo da bolsa ser computado.")
    valor: float = Field(..., title="Valor", description="Valor da compra.")
    data: datetime = Field(
        ...,
        title="Data",
        description="Data da compra.",
        default_factory=obter_data_atual,
    )


class TransacaoRegistrada(TransacaoSimples):
    id: int = Field(..., title="ID", description="ID da transação.")


class SolicitacaoTransacao(BaseModel):
    ativos: List[str] = Field(
        ..., title="Ativos", description="Lista de ativos da bolsa a ser computado."
    )
    quantidadeAtivos: int = Field(
        ...,
        title="Quantidade de ativos",
        description="Quantidade de ativos da bolsa a ser computado.",
    )
