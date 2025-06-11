from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
import uuid

from domain.entities.pedido import Pedido, StatusPedido

class IPedidoRepository:
    @abstractmethod
    async def salvar(self, pedido: Pedido) -> Pedido:
        """Salva um novo pedido ou atualiza um existente(incluindo seus itens)."""
        pass
    
    @abstractmethod
    async def buscar_por_id(self, pedido_id: uuid.UUID)-> Optional[Pedido]:
        """Busca um pedido completo (com seus itens) pelo seu ID."""
        pass
    
    @abstractmethod
    async def listar_por_cliente_id(
        self,
        cliente_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        data_inicio: Optional[datetime] = None,
        data_fim: Optional[datetime] = None,
        status: Optional[List[str]] = None
    ) -> List[Pedido]:
        """Lista todos os pedidos de um restaurante específico, com filtros opcionais"""
        pass
    
    @abstractmethod
    async def listar_por_status(
        self,
        status_lista: list[str],
        skip: int = 0,
        limit: int = 100,
        data_inicio:Optional[datetime] = None,
        data_fim:Optional[datetime] = None
    )-> List[Pedido]:
        """Lista pedidos filtrando por uma lista de status"""
        pass
    
    # Não incluiremos um método 'deletar' para Pedido por enquanto,
    # pois pedidos geralmente são arquivados ou cancelados (mudança de status),
    # mas não fisicamente deletados devido a registros históricos e financeiros.
    # Se a deleção física for um requisito, um método pode ser adicionado.
    
