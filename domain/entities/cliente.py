# delivery_api_project/domain/entities/cliente.py

import uuid
from datetime import datetime
from typing import List, Optional

from domain.value_objects.endereco import Endereco # Importamos nosso Value Object

class Cliente:
    def __init__(self,
                 nome: str,
                 email: str,
                 senha_hash: str,
                 cliente_id: Optional[int] = None, # Corrigido para uuid.UUID
                 telefone: Optional[str] = None,
                 enderecos: Optional[List[Endereco]] = None, # Agora usamos o tipo Endereco
                 data_criacao: Optional[datetime] = None
                 ):
        self.id: uuid.UUID = cliente_id if cliente_id else uuid.uuid4()
        self.nome: str = nome
        self.email: str = email
        self.senha_hash: str = senha_hash
        self.telefone: Optional[str] = telefone
        self.enderecos: List[Endereco] = enderecos if enderecos is not None else []
        self.data_criacao: datetime = data_criacao if data_criacao else datetime.utcnow()

    def adicionar_endereco(self, endereco: Endereco):
        if not isinstance(endereco, Endereco):
            raise TypeError("Apenas objetos Endereco podem ser adicionados.")
        if endereco not in self.enderecos: # Evita endereços duplicados (baseado na igualdade estrutural)
            self.enderecos.append(endereco)
        # Poderíamos adicionar regras de negócio aqui, como um limite máximo de endereços.

    def remover_endereco(self, endereco: Endereco):
        try:
            self.enderecos.remove(endereco) # Funciona devido à igualdade estrutural de Endereco
        except ValueError:
            # Endereço não encontrado, podemos decidir se lançamos um erro ou ignoramos
            pass

    # def is_ativo(self) -> bool:
    #     # Lógica para verificar se o cliente está ativo
    #     return True

    def __eq__(self, other):
        if not isinstance(other, Cliente):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)