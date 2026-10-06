from typing import Dict
from .pessoa import Pessoa

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