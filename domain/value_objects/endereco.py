from dataclasses import dataclass, field
from typing import Optional

# Futuramente, poderíamos ter um Value Object CoordenadaGeo
# from.coordenada_geo import CoordenadaGeo

@dataclass(frozen=True) # frozen=True torna a classe imutável
class Endereco:
    logradouro: str
    numero: str
    bairro: str
    cidade: str
    estado: str # Sigla da UF, ex: "SP"
    cep: str    # Código de Endereçamento Postal

    # Atributos opcionais devem vir depois dos obrigatórios ou ter um valor padrão
    complemento: Optional[str] = None
    # coordenadas: Optional[CoordenadaGeo] = None # Para geolocalização

    def __post_init__(self):
        # Validações podem ser adicionadas aqui para garantir a integridade do objeto
        # Exemplo simples:
        if not self.logradouro.strip():
            raise ValueError("Logradouro não pode ser vazio.")
        if not self.numero.strip():
            raise ValueError("Número não pode ser vazio.")
        if not self.bairro.strip():
            raise ValueError("Bairro não pode ser vazio.")
        if not self.cidade.strip():
            raise ValueError("Cidade não pode ser vazia.")
        if not self.estado.strip() or len(self.estado)!= 2: # Exemplo de validação de UF
            raise ValueError("Estado (UF) inválido.")
        if not self.cep.strip(): # Validação de CEP poderia ser mais robusta (formato)
            raise ValueError("CEP não pode ser vazio.")

    def formatar_endereco_completo(self) -> str:
        """Retorna uma string formatada do endereço completo."""
        partes = [f"{self.logradouro}, {self.numero}"]
        if self.complemento:
            partes.append(self.complemento)
        partes.append(self.bairro)
        partes.append(f"{self.cidade} - {self.estado}")
        partes.append(f"CEP: {self.cep}")
        return " | ".join(partes)

 