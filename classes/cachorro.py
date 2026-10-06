from typing import List
from .animal import Animal


class Cachorro(Animal):
    """Representa um cachorro disponível para adoção."""
    def __init__(self, id_animal: str, raca: str, nome: str, sexo: str, 
                 idade_meses: int, porte: str, temperamento: List[str], 
                 data_entrada: str, necessidade_passeio: str):
        super().__init__(id_animal, raca, nome, sexo, idade_meses, porte, temperamento, data_entrada)
        self.especie = "cachorro"
        self.necessidade_passeio = necessidade_passeio