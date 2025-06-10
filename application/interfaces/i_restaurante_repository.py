from abc import ABC, abstractmethod
from typing import List, Optional
import uuid

from domain.entities.restaurante import Restaurante

class IRestauranteRepository(ABC):
    
    @abstractmethod
    async def salvar(self, restaurante: Restaurante) -> Restaurante:
        """Salva um novo restaurante ou atualiza um existente"""
        pass
    
    @abstractmethod
    async def buscar_por_id(self, restaurande_id: uuid.UUID) -> Optional[int]:
        """Busca um restaurante pelo seu ID."""
        pass
    
    @abstractmethod
    async def buscar_por_cnpj(self, cnpj: str) -> Optional[str]:
        """Buscar um restaurante pelo seu CNPJ"""
        pass
    
    @abstractmethod
    async def listar_todos(self, skip: int = 0, limit: int = 100) -> List:
        """Lista todos os restaurantes com paginação."""
        pass
    
    @abstractmethod
    async def listar_ativo_por_nome_ou_categoria(
        self,
        termo_busca: Optional[str] = None,
        categoria_busca: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
        ) -> List:
        """Lista restaurantes ativos filtrando por nome ou categoria"""
        pass
    
    @abstractmethod
    async def deletar(self, restaurante_id: uuid.UUID) -> bool:
        "Deleta um restaurante pelo seu ID"
        pass
