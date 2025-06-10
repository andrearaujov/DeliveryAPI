import uuid
from datetime import datetime
from typing import Optional

class CategoriaProduto:
    def __init__(self,
                 restaurante_id: uuid.UUID,
                 nome: str,
                 categoria_produto_id: Optional[int] = None,
                 descricao: Optional[str] = None,
                 ordem: Optional[int] = 0, # Padrão para ordem, se não especificado
                 data_criacao: Optional[datetime] = None,
                 data_atualizacao: Optional[datetime] = None
                 ):
        self.id: uuid.UUID = categoria_produto_id if categoria_produto_id is not None else uuid.uuid4()
        self.restaurante_id: uuid.UUID = restaurante_id # FK para Restaurante
        self.nome: str = nome
        self.descricao: Optional[str] = descricao
        self.ordem: Optional[int] = ordem

        now = datetime.utcnow()
        self.data_criacao: datetime = data_criacao if data_criacao is not None else now
        self.data_atualizacao: datetime = data_atualizacao if data_atualizacao is not None else now

        # Validações
        if not restaurante_id:
            raise ValueError("ID do restaurante é obrigatório para a categoria.")
        if not nome.strip():
            raise ValueError("Nome da categoria não pode ser vazio.")

    def atualizar_detalhes(self,
                           nome: Optional[str] = None,
                           descricao: Optional[str] = None,
                           ordem: Optional[int] = None):
        """Atualiza os detalhes da categoria de produto."""
        if nome is not None:
            if not nome.strip():
                raise ValueError("Nome da categoria não pode ser vazio ao atualizar.")
            self.nome = nome
        
        # Permitir definir descrição como None ou string vazia
        if descricao is not None:
            self.descricao = descricao
        
        if ordem is not None:
            self.ordem = ordem
            
        self.data_atualizacao = datetime.utcnow()

    def __eq__(self, other):
        if not isinstance(other, CategoriaProduto):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)