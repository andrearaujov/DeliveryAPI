import uuid
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Optional

# Futuramente, poderíamos ter uma entidade ou VO para CategoriaProduto
# from.categoria_produto import CategoriaProduto

class Produto:
    def __init__(self,
                 restaurante_id: uuid.UUID,
                 nome: str,
                 descricao: str,
                 preco: Decimal,
                 produto_id: Optional[int] = None,
                 imagem_url: Optional[str] = None,
                 disponivel: bool = True,
                 # categoria_produto_id: Optional = None, # Se CategoriaProduto for uma entidade
                 categoria_produto_nome: Optional[str] = None, # Ou um nome de categoria simples
                 data_criacao: Optional[datetime] = None,
                 data_atualizacao: Optional[datetime] = None
                 ):
        self.id: uuid.UUID = produto_id if produto_id is not None else uuid.uuid4()
        self.restaurante_id: uuid.UUID = restaurante_id # FK para Restaurante
        self.nome: str = nome
        self.descricao: str = descricao
        
        try:
            if not isinstance(preco, Decimal):
                preco = Decimal(str(preco)) # Tenta converter se não for Decimal
            if preco <= Decimal('0'):
                raise ValueError("Preço deve ser positivo.")
            self.preco: Decimal = preco
        except InvalidOperation:
            raise ValueError("Formato de preço inválido.")
            
        self.imagem_url: Optional[str] = imagem_url
        self.disponivel: bool = disponivel
        # self.categoria_produto_id: Optional = categoria_produto_id
        self.categoria_produto_nome: Optional[str] = categoria_produto_nome
        
        now = datetime.utcnow()
        self.data_criacao: datetime = data_criacao if data_criacao is not None else now
        self.data_atualizacao: datetime = data_atualizacao if data_atualizacao is not None else now

        # Validações
        if not restaurante_id: # restaurante_id é obrigatório
            raise ValueError("ID do restaurante é obrigatório.")
        if not nome.strip():
            raise ValueError("Nome do produto não pode ser vazio.")
        # Descrição pode ser vazia, mas não None se for obrigatória (ajustar conforme regra)

    def atualizar_detalhes(self,
                           nome: Optional[str] = None,
                           descricao: Optional[str] = None,
                           preco: Optional[float] = None,
                           imagem_url: Optional[str] = None,
                           # categoria_produto_id: Optional = None,
                           categoria_produto_nome: Optional[str] = None
                           ):
        """Atualiza os detalhes do produto."""
        if nome is not None:
            if not nome.strip():
                raise ValueError("Nome do produto não pode ser vazio ao atualizar.")
            self.nome = nome
        if descricao is not None:
            self.descricao = descricao # Permitir descrição vazia se for o caso
        if preco is not None:
            try:
                if not isinstance(preco, Decimal):
                    preco = Decimal(str(preco))
                if preco <= Decimal('0'):
                    raise ValueError("Preço deve ser positivo ao atualizar.")
                self.preco = preco
            except InvalidOperation:
                raise ValueError("Formato de preço inválido ao atualizar.")
        if imagem_url is not None: # Permitir definir como None para remover imagem
            self.imagem_url = imagem_url
        # if categoria_produto_id is not None:
        #     self.categoria_produto_id = categoria_produto_id
        if categoria_produto_nome is not None:
            self.categoria_produto_nome = categoria_produto_nome
            
        self.data_atualizacao = datetime.utcnow()

    def marcar_como_disponivel(self):
        self.disponivel = True
        self.data_atualizacao = datetime.utcnow()

    def marcar_como_indisponivel(self):
        self.disponivel = False
        self.data_atualizacao = datetime.utcnow()

    def __eq__(self, other):
        if not isinstance(other, Produto):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)