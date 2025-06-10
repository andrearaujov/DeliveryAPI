from abc import ABC, abstractmethod
from typing import List, Optional
import uuid

from domain.entities.produto import Produto

class IProdutoRepository(ABC):
    
    @abstractmethod
    async def salvar(self, produto:Produto) -> Produto:
        """Saçvar um novo produto ou atualiza um existente"""
    pass

    @abstractmethod
    async def buscar_por_id(self, produto_id: uuid.UUID) -> Optional[Produto]:
        """Busca um produto pelo seu ID."""
    pass

    @abstractmethod
    
    async def listar_por_restaurande_id(
        self,
        restaurante_id: uuid.UUID,
        disponivel_apenas: bool = False, #Opção para filtrar por disponibilidade
        skip: int = 0,
        limit: int = 100
    ) -> Optional[Produto]:
        """Lista todos os produtos de um restaurante específicos"""
        
        @abstractmethod
        async def listar_por_categoria_id_e_restaurante_id(
            self,
            categoria_id: uuid.UUID,
            restaurante_id: uuid.UUID,
            disponivel_apenas: bool = False,
            skip: int = 0,
            limit: int = 100
        ) ->List[Produto]:
            """Lista todos os produtos de uma categoria específica em um restaurante"""
        pass
    
    
    @abstractmethod
    async def deletar(self, produto_id: uuid.UUID) -> bool:
        """Deleta um produto pelo seu ID"""   
    pass
    


    
    
