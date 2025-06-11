from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
import uuid

@dataclass(frozen=True)
class AdicionarProdutoRequestDTO:
    restaurante_id: uuid.UUID
    nome:str
    descricao: str
    preco: Decimal
    categoria_produto_id:Optional[int] = None
    imagem_url: Optional[str] = None
    disponivel: bool = True