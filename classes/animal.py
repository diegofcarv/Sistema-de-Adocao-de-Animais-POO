from abc import ABC
from typing import List
from .status_animal import StatusAnimal
from .vacinavel_mixin import VacinavelMixin
from .adestravel_mixin import AdestravelMixin

class Animal(ABC, VacinavelMixin, AdestravelMixin):
    """Classe abstrata que representa um animal do sistema."""
    
    def __init__(self, id_animal: str, raca: str, nome: str, sexo: str, 
                 idade_meses: int, porte: str, temperamento: List[str], data_entrada: str):
        self.id_animal = id_animal
        self.raca = raca
        self.nome = nome
        self.sexo = sexo
        self.temperamento = temperamento
        self.data_entrada = data_entrada
        self.status = StatusAnimal.DISPONIVEL
        self.historico_eventos: List[str] = []
        
        self.idade_meses = idade_meses
        self.porte = porte

    @property
    def idade_meses(self) -> int:
        """int: Idade do animal em meses."""
        return self._idade_meses

    @idade_meses.setter
    def idade_meses(self, valor: int) -> None:
        if valor < 0:
            raise ValueError("A idade do animal não pode ser negativa.")
        self._idade_meses = valor

    @property
    def porte(self) -> str:
        """str: Porte do animal (P, M ou G)."""
        return self._porte

    @porte.setter
    def porte(self, valor: str) -> None:
        if valor not in ["P", "M", "G"]:
            raise ValueError("O porte deve ser obrigatoriamente 'P', 'M' ou 'G'.")
        self._porte = valor

    def registrar_evento(self, evento: str) -> None:
        """Adiciona um evento ao histórico do animal."""
        self.historico_eventos.append(evento)

    def mudar_status(self, novo_status: StatusAnimal) -> None:
        """Altera o status do animal e registra no histórico."""
        self.status = novo_status
        self.registrar_evento(f"Status alterado para {novo_status.value}")

    def __str__(self) -> str:
        return f"{self.nome} ({getattr(self, 'especie', 'animal')} - {self.raca}) - Status: {self.status.value}"

    def __repr__(self) -> str:
        return f"Animal(id='{self.id_animal}', nome='{self.nome}')"

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Animal):
            return NotImplemented
        return self.id_animal == outro.id_animal

    def __hash__(self) -> int:
        return hash(self.id_animal)

    def __lt__(self, outro: object) -> bool:
        if not isinstance(outro, Animal):
            return NotImplemented
        return self.data_entrada < outro.data_entrada

    def __iter__(self):
        """Permite iterar pelo histórico de eventos do animal."""
        return iter(self.historico_eventos)