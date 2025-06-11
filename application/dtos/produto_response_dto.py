from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
import uuid
from datetime import datetime

@dataclass(froze=True)
class ProdutoResponseDTO:
    id: uuid.UUID
    restaurante_id: uuid.UUID
    nome:str
    descricao: str
    preco: Decimal
    categoria_produto_id: Optional[int]
    imagem_url: Optional[str]
    disponivel: bool
    data_criacao:datetime
    data_atualizacao:datetime