from abc import ABC, abstractmethod
from typing import List, Optional
import uuid

from domain.entities.categoria_produto import CategoriaProduto

class ICategoriaProdutoRepository(ABC):
    
    @abstractmethod
    async def salvar(self, categoria: CategoriaProduto) -> CategoriaProduto:
        """Salva uma nova categoria ou atualiza uma existente."""
    pass

    @abstractmethod
    async def buscar_por_id(self, categoria_id: uuid.UUID) -> Optional[CategoriaProduto]:
        """Busca uma categoria de um produto pelo seu ID."""
    pass
        
    @abstractmethod
    async def listar_por_restaurante_id(
        self, 
        restaurante_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100
    ) ->List[CategoriaProduto]:
        """Lista todas as categorias de produto de um restaurante específico"""
    pass
        
    @abstractmethod
    async def buscar_por_nome_e_restaurande_id(
        self,
        nome: str,
        restaurante_id= uuid.UUID) -> Optional[CategoriaProduto]:
        """Buscar uma categoria pelo nome dentro de um restaurante específico"""
        pass
        
    @abstractmethod
    async def deleter(self, categoria_id: uuid.UUID) -> bool:
        """Deleta uma categoria de produto pelo seu ID."""
    pass
        