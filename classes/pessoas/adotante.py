from typing import Dict, TYPE_CHECKING
from .pessoa import Pessoa

if TYPE_CHECKING:
    from ..animais.animal import Animal

class Adotante(Pessoa):
    """Representa uma pessoa interessada em adotar um animal."""

    def __init__(self, cpf: str, nome: str, idade: int, telefone: str, email: str,
                 moradia: str, area_util: float, experiencia_pets: bool,
                 criancas: Dict, outros_animais: Dict, experiencia_anterior: Dict):
        super().__init__(cpf, nome, idade, telefone, email)
        self.area_util = area_util
        self.experiencia_pets = experiencia_pets
        self.criancas = criancas
        self.outros_animais = outros_animais
        self.experiencia_anterior = experiencia_anterior
        self.moradia = moradia

    @property
    def moradia(self) -> str:
        """str: Tipo de moradia ('casa' ou 'apto')."""
        return self._moradia

    @moradia.setter
    def moradia(self, valor: str) -> None:
        if valor not in ["casa", "apto"]:
            raise ValueError("Moradia deve ser 'casa' ou 'apto'.")
        self._moradia = valor

    def calcular_pontuacao_compatibilidade(self, animal: "Animal") -> float:
        """
        Calcula a pontuação de compatibilidade (0–100) entre o adotante e um animal.

        Os critérios ponderados são:
        - Porte x moradia/área útil          (peso 30)
        - Experiência com pets               (peso 20)
        - Presença de crianças x temperamento (peso 20)
        - Outros animais em casa             (peso 15)
        - Experiência anterior               (peso 15)

        Args:
            animal (Animal): O animal a ser avaliado.

        Returns:
            float: Pontuação de 0 a 100.
        """
        pontos = 0.0

        # --- Critério 1: Porte x moradia/área útil (peso 30) ---
        porte = animal.porte
        if porte == "P":
            pontos += 30
        elif porte == "M":
            if self.moradia == "casa":
                pontos += 30
            else:
                pontos += 15 if self.area_util >= 50 else 5
        elif porte == "G":
            if self.moradia == "casa" and self.area_util >= 80:
                pontos += 30
            elif self.moradia == "casa":
                pontos += 15
            else:
                pontos += 0

        # --- Critério 2: Experiência com pets (peso 20) ---
        if self.experiencia_pets:
            pontos += 20
        else:
            pontos += 5

        # --- Critério 3: Crianças x temperamento do animal (peso 20) ---
        tem_criancas = self.criancas.get("tem_criancas", False)
        temperamento = [t.lower() for t in animal.temperamento]

        if tem_criancas:
            temperamentos_ariscos = {"arisco", "agressivo", "nervoso", "territorial"}
            if temperamentos_ariscos.intersection(temperamento):
                pontos += 0
            else:
                pontos += 20
        else:
            pontos += 20

        # --- Critério 4: Outros animais em casa (peso 15) ---
        tem_outros = self.outros_animais.get("tem_outros", False)
        if not tem_outros:
            pontos += 15
        else:
            porte_outros = self.outros_animais.get("porte", "P")
            if porte == "P" or porte_outros == "P":
                pontos += 10
            else:
                pontos += 5

        # --- Critério 5: Experiência anterior (peso 15) ---
        quantidade_anterior = self.experiencia_anterior.get("quantidade", 0)
        if quantidade_anterior >= 2:
            pontos += 15
        elif quantidade_anterior == 1:
            pontos += 10
        else:
            pontos += 0

        return round(min(pontos, 100.0), 2)
