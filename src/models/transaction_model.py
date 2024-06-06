from pydantic import BaseModel, Field

from utils.models_utils import obter_data_atual, obter_uuid


class TransacaoSimples(BaseModel):
    id: str = Field(
        ..., title="ID", description="ID da transação.", default_factory=obter_uuid
    )
    ativo: str = Field(..., title="Ativo", description="Ativo da bolsa ser computado.")
    valor: float = Field(..., title="Valor", description="Valor da compra.")
    data: str = Field(
        ...,
        title="Data",
        description="Data da compra.",
        default_factory=obter_data_atual,
    )
