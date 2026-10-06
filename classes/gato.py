from typing import List
from .animal import Animal

class Gato(Animal):
    """Representa um gato disponível para adoção."""
    def __init__(self, id_animal: str, raca: str, nome: str, sexo: str, 
                 idade_meses: int, porte: str, temperamento: List[str], 
                 data_entrada: str, independencia: str):
        super().__init__(id_animal, raca, nome, sexo, idade_meses, porte, temperamento, data_entrada)
        self.especie = "gato"
        self.independencia = independencia