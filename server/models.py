from pydantic import BaseModel
from typing import Any, List

class PaginacaoResponse(BaseModel):
    data: List[Any]
    total: int
    page: int
    limit: int
    total_pages: int

class EstatisticasResponse(BaseModel):
    total_despesas: float
    media_despesas: float
    total_operadoras: int
    top_5_operadoras: list
