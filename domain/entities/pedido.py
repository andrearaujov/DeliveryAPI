# delivery_api_project/domain/entities/pedido.py

import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from domain.entities.item_pedido import ItemPedido
from domain.value_objects.endereco import Endereco

# Definição de StatusPedido (poderia ser um Enum em Python 3.x)
class StatusPedido:
    PENDENTE = "PENDENTE"
    CONFIRMADO_PELO_RESTAURANTE = "CONFIRMADO_PELO_RESTAURANTE"
    EM_PREPARO = "EM_PREPARO"
    PRONTO_PARA_COLETA = "PRONTO_PARA_COLETA"
    SAIU_PARA_ENTREGA = "SAIU_PARA_ENTREGA"
    ENTREGUE = "ENTREGUE"
    CANCELADO_PELO_CLIENTE = "CANCELADO_PELO_CLIENTE"
    CANCELADO_PELO_RESTAURANTE = "CANCELADO_PELO_RESTAURANTE"
    TODOS_OS_STATUS = [PENDENTE, CONFIRMADO_PELO_RESTAURANTE, EM_PREPARO, PRONTO_PARA_COLETA, SAIU_PARA_ENTREGA, ENTREGUE, CANCELADO_PELO_CLIENTE, CANCELADO_PELO_RESTAURANTE]
    PODE_MODIFICAR_ITENS = [PENDENTE]
    PODE_CANCELAR_PELO_CLIENTE = [PENDENTE, CONFIRMADO_PELO_RESTAURANTE, EM_PREPARO, PRONTO_PARA_COLETA, SAIU_PARA_ENTREGA]
    STATUS_QUE_NAO_PODEM_SER_CANCELADOS_PELO_RESTAURANTE = [ENTREGUE, CANCELADO_PELO_CLIENTE, CANCELADO_PELO_RESTAURANTE]



class Pedido:
    def __init__(self,
                 cliente_id: uuid.UUID,
                 restaurante_id: uuid.UUID,
                 endereco_entrega: Endereco,
                 pedido_id: Optional[int] = None,
                 itens: Optional[List[ItemPedido]] = None,
                 status_pedido: str = StatusPedido.PENDENTE,
                 taxa_entrega: Decimal = Decimal('0.00'),
                 metodo_pagamento: Optional[str] = None,
                 observacoes_gerais: Optional[str] = None,
                 entregador_id: Optional[int] = None,
                 data_criacao: Optional[datetime] = None,
                 data_ultima_atualizacao: Optional[datetime] = None
                 ):
        self.id: uuid.UUID = pedido_id if pedido_id is not None else uuid.uuid4()
        self.cliente_id: uuid.UUID = cliente_id
        self.restaurante_id: uuid.UUID = restaurante_id
        self.endereco_entrega: Endereco = endereco_entrega
        self._itens: List[ItemPedido] = itens if itens is not None else []

        if status_pedido not in StatusPedido.TODOS_OS_STATUS:
            raise ValueError(f"Status do pedido inválido: {status_pedido}")
        self.status_pedido: str = status_pedido
        
        self.taxa_entrega: Decimal = self._validar_decimal_nao_negativo(taxa_entrega, "Taxa de entrega")
        self.metodo_pagamento: Optional[str] = metodo_pagamento
        self.observacoes_gerais: Optional[str] = observacoes_gerais
        self.entregador_id: Optional[int] = entregador_id

        now = datetime.utcnow()
        self.data_criacao: datetime = data_criacao if data_criacao is not None else now
        self.data_ultima_atualizacao: datetime = data_ultima_atualizacao if data_ultima_atualizacao is not None else now

        if not cliente_id:
            raise ValueError("ID do cliente é obrigatório.")
        if not restaurante_id:
            raise ValueError("ID do restaurante é obrigatório.")
        if not isinstance(endereco_entrega, Endereco):
            raise TypeError("Endereço de entrega deve ser um objeto Endereco válido.")

    def _validar_decimal_nao_negativo(self, valor: Decimal, nome_campo: str) -> Decimal:
        try:
            if not isinstance(valor, Decimal):
                valor = Decimal(str(valor))
            if valor < Decimal('0'):
                raise ValueError(f"{nome_campo} não pode ser negativo.")
            return valor
        except Exception: # InvalidOperation
            raise ValueError(f"Formato de {nome_campo} inválido.")

    @property
    def itens(self) -> List[ItemPedido]:
        return list(self._itens)

    @property
    def valor_subtotal_itens(self) -> Decimal:
        return sum(item.preco_total_item for item in self._itens) if self._itens else Decimal('0.00')

    @property
    def valor_total_pedido(self) -> Decimal:
        return self.valor_subtotal_itens + self.taxa_entrega

    def adicionar_item(self, item: ItemPedido):
        if not isinstance(item, ItemPedido):
            raise TypeError("Apenas objetos ItemPedido podem ser adicionados.")
        if self.status_pedido not in StatusPedido.PODE_MODIFICAR_ITENS:
            raise ValueError(f"Não é possível adicionar itens a um pedido com status {self.status_pedido}")
        
        self._itens.append(item)
        self.data_ultima_atualizacao = datetime.utcnow()

    def remover_item(self, item_id: uuid.UUID):
        if self.status_pedido not in StatusPedido.PODE_MODIFICAR_ITENS:
            raise ValueError(f"Não é possível remover itens de um pedido com status {self.status_pedido}")
        
        item_encontrado = next((i for i in self._itens if i.id == item_id), None)
        if item_encontrado:
            self._itens.remove(item_encontrado)
            self.data_ultima_atualizacao = datetime.utcnow()
        else:
            raise ValueError(f"Item com ID {item_id} não encontrado no pedido.")

    def _atualizar_status(self, novo_status: str):
        if novo_status not in StatusPedido.TODOS_OS_STATUS:
            raise ValueError(f"Novo status do pedido inválido: {novo_status}")
        
        # Aqui viria a lógica de máquina de estados para transições válidas
        # Exemplo muito simples:
        if self.status_pedido == StatusPedido.ENTREGUE and novo_status!= StatusPedido.ENTREGUE:
            raise ValueError("Pedido entregue não pode ter seu status alterado (exceto para correções específicas).")
        if self.status_pedido == StatusPedido.CANCELADO_PELO_CLIENTE and novo_status!= StatusPedido.CANCELADO_PELO_CLIENTE:
            raise ValueError("Pedido cancelado pelo cliente não pode ter seu status alterado.")
        if self.status_pedido == StatusPedido.CANCELADO_PELO_RESTAURANTE and novo_status!= StatusPedido.CANCELADO_PELO_RESTAURANTE:
            raise ValueError("Pedido cancelado pelo restaurante não pode ter seu status alterado.")

        self.status_pedido = novo_status
        self.data_ultima_atualizacao = datetime.utcnow()

    def confirmar_pelo_restaurante(self):
        if self.status_pedido!= StatusPedido.PENDENTE:
            raise ValueError(f"Pedido só pode ser confirmado pelo restaurante se estiver PENDENTE. Status atual: {self.status_pedido}")
        self._atualizar_status(StatusPedido.CONFIRMADO_PELO_RESTAURANTE)

    def marcar_como_em_preparo(self):
        if self.status_pedido!= StatusPedido.CONFIRMADO_PELO_RESTAURANTE:
            raise ValueError(f"Pedido só pode ir para EM PREPARO se estiver CONFIRMADO PELO RESTAURANTE. Status atual: {self.status_pedido}")
        self._atualizar_status(StatusPedido.EM_PREPARO)
    
    def marcar_como_pronto_para_coleta(self):
        if self.status_pedido!= StatusPedido.EM_PREPARO:
            raise ValueError(f"Pedido só pode ir para PRONTO PARA COLETA se estiver EM PREPARO. Status atual: {self.status_pedido}")
        self._atualizar_status(StatusPedido.PRONTO_PARA_COLETA)

    def marcar_como_saiu_para_entrega(self, entregador_id: uuid.UUID):
        if self.status_pedido!= StatusPedido.PRONTO_PARA_COLETA: # Ou EM_PREPARO se o restaurante mesmo entrega
            raise ValueError(f"Pedido só pode SAIR PARA ENTREGA se estiver PRONTO PARA COLETA. Status atual: {self.status_pedido}")
        if not entregador_id:
            raise ValueError("ID do entregador é obrigatório para marcar como saiu para entrega.")
        self.entregador_id = entregador_id
        self._atualizar_status(StatusPedido.SAIU_PARA_ENTREGA)

    def marcar_como_entregue(self):
        if self.status_pedido!= StatusPedido.SAIU_PARA_ENTREGA:
            raise ValueError(f"Pedido só pode ser marcado como ENTREGUE se estiver SAIU PARA ENTREGA. Status atual: {self.status_pedido}")
        self._atualizar_status(StatusPedido.ENTREGUE)

    def cancelar_pelo_cliente(self):
        if self.status_pedido not in StatusPedido.PODE_CANCELAR_PELO_CLIENTE:
            raise ValueError(f"Pedido com status {self.status_pedido} não pode ser cancelado pelo cliente.")
        self._atualizar_status(StatusPedido.CANCELADO_PELO_CLIENTE)

    def cancelar_pelo_restaurante(self, motivo: str): # Restaurante deve fornecer um motivo
        if self.status_pedido in StatusPedido.STATUS_QUE_NAO_PODEM_SER_CANCELADOS_PELO_RESTAURANTE:
            raise ValueError(f"Pedido com status {self.status_pedido} não pode ser cancelado pelo restaurante.")
        if not motivo or not motivo.strip():
            raise ValueError("Um motivo é obrigatório para o restaurante cancelar o pedido.")
        # Poderíamos armazenar o 'motivo' em algum lugar
        self.observacoes_gerais = f"Cancelado pelo restaurante: {motivo}" + (f" | {self.observacoes_gerais}" if self.observacoes_gerais else "")
        self._atualizar_status(StatusPedido.CANCELADO_PELO_RESTAURANTE)

    def __eq__(self, other):
        if not isinstance(other, Pedido):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)