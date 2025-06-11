import uuid
from decimal import Decimal, InvalidOperation
from typing import Optional

class ItemPedido:
    def __init__(self,
                 produto_id: uuid.UUID,
                 quantidade: int,
                 preco_unitario_compra: Decimal,
                 item_pedido_id: Optional[int] = None,
                 observacoes_item: Optional[str] = None
                ):
        self.id: uuid.UUID = item_pedido_id if item_pedido_id is not None else uuid.uuid4()
        self.produto_id: uuid.UUID = produto_id
        
        if not isinstance(quantidade, int) or quantidade <=0:
            raise ValueError("Quantidade deve ser um inteiro positivo.")
        self.quantidade: int=quantidade
        
        try: 
            if not isinstance(preco_unitario_compra, Decimal):
                preco_unitario_compra = Decimal(str(preco_unitario_compra))
            if preco_unitario_compra < Decimal('0'): #Não permite preço zero
                raise ValueError("Preço unitário no momento da compra deve ser positivo")
            self.preco_unitario_compra: Decimal = preco_unitario_compra
        except InvalidOperation:
            raise ValueError("Formato de preço unitário inválido.")
        
        self.observacoes_item: Optional[str] = observacoes_item
        
        @property
        def preco_total_item(self) -> Decimal:
            """Calcula o preço total deste item."""
            return self.quantidade* self.preco_unitario_compra
        
        def atualizar_quantidade(self, nova_quantidade: int):
            if not isinstance(nova_quantidade, int) or nova_quantidade <=0:
                raise ValueError("Nova quantidade deve ser um inteiro positivo")
            self.quantidade = nova_quantidade
             # Nota: Se o item já faz parte de um pedido, o Pedido (Aggregate Root)
        # deveria ser responsável por recalcular o valor total do pedido.

        def adicionar_observacao(self, observacao: str):
            self.observacao_item = observacao
            
        def __eq__(self, other):
            if not isinstance(other, ItemPedido):
                return False
       
            return self.id == other.id
        
        def __hash__(self):
            return hash(self.id)       