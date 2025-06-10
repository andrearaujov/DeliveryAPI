import uuid
from datetime import datetime
from typing import List, Optional

from domain.value_objects.endereco import Endereco

# Futuramente, poderíamos ter uma entidade ou VO para CategoriaRestaurante
# from.categoria_restaurante import CategoriaRestaurante

class Restaurante:
    def __init__(self,
                 nome_fantasia: str,
                 cnpj: str, # Adicionar validação de formato de CNPJ posteriormente
                 email_contato: str, # Adicionar validação de formato de email
                 endereco: Endereco,
                 restaurante_id: Optional[int] = None,
                 categorias: Optional[List[str]] = None, # Simples lista de strings por enquanto
                 horario_funcionamento: Optional[str] = "08:00-22:00", # Exemplo simples
                 tempo_medio_preparo_min: Optional[int] = 30,
                 ativo: bool = True,
                 data_criacao: Optional[datetime] = None
                 ):
        self.id: uuid.UUID = restaurante_id if restaurante_id is not None else uuid.uuid4()
        self.nome_fantasia: str = nome_fantasia
        self.cnpj: str = cnpj
        self.email_contato: str = email_contato
        self.endereco: Endereco = endereco
        self.categorias: List[str] = categorias if categorias is not None else []
        self.horario_funcionamento: Optional[str] = horario_funcionamento
        self.tempo_medio_preparo_min: Optional[int] = tempo_medio_preparo_min
        self.ativo: bool = ativo
        self.data_criacao: datetime = data_criacao if data_criacao is not None else datetime.utcnow()

        # Validações iniciais
        if not nome_fantasia.strip():
            raise ValueError("Nome fantasia não pode ser vazio.")
        if not cnpj.strip(): # Validação de CNPJ mais robusta seria ideal
            raise ValueError("CNPJ não pode ser vazio.")
        if not email_contato.strip(): # Validação de email mais robusta seria ideal
            raise ValueError("Email de contato não pode ser vazio.")
        if not isinstance(endereco, Endereco):
            raise TypeError("Endereço deve ser um objeto Endereco válido.")

    def ativar(self):
        """Ativa o restaurante para receber pedidos."""
        self.ativo = True

    def desativar(self):
        """Desativa o restaurante (não recebe mais pedidos)."""
        self.ativo = False

    def atualizar_horario_funcionamento(self, novo_horario: str):
        self.horario_funcionamento = novo_horario

    def adicionar_categoria(self, categoria: str):
        if categoria and categoria.strip() and categoria not in self.categorias:
            self.categorias.append(categoria)

    def remover_categoria(self, categoria: str):
        try:
            self.categorias.remove(categoria)
        except ValueError:
            pass # Categoria não encontrada

    def __eq__(self, other):
        if not isinstance(other, Restaurante):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)