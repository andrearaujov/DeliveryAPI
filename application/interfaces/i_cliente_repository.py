from abc import ABC, abstractmethod
from typing import List, Optional
import uuid

from domain.entities.cliente import Cliente

class IClienteRepository(ABC):

    @abstractmethod
    async def salvar(self, cliente: Cliente) -> Cliente:
        """Salva um novo cliente ou atualiza um existente."""
        pass

    @abstractmethod
    async def buscar_por_id(self, cliente_id: uuid.UUID) -> Optional[Cliente]:
        """Busca um cliente pelo seu ID."""
        pass

    @abstractmethod
    async def buscar_por_email(self, email: str) -> Optional[Cliente]:
        """Busca um cliente pelo seu email."""
        pass

    @abstractmethod
    async def listar_todos(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """Lista todos os clientes com paginação."""
        pass

    @abstractmethod
    async def deletar(self, cliente_id: uuid.UUID) -> bool:
        """Deleta um cliente pelo seu ID. Retorna True se bem sucedido."""
        pass