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

    def para_dict(self) -> dict:
        """Converte o gato em dicionário para persistência."""
        return {
            "especie": "gato",
            "id_animal": self.id_animal,
            "raca": self.raca,
            "nome": self.nome,
            "sexo": self.sexo,
            "idade_meses": self.idade_meses,
            "porte": self.porte,
            "temperamento": self.temperamento,
            "data_entrada": self.data_entrada,
            "independencia": self.independencia,
            "status": self.status.value,
            "historico_eventos": self.historico_eventos,
            "historico_vacinas": getattr(self, "historico_vacinas", []),
            "nivel_adestramento": getattr(self, "nivel_adestramento", ""),
        }

    @classmethod
    def de_dict(cls, dados: dict) -> "Gato":
        """Reconstrói um Gato a partir de um dicionário."""
        from ..status_animal import StatusAnimal
        obj = cls(
            id_animal=dados["id_animal"],
            raca=dados["raca"],
            nome=dados["nome"],
            sexo=dados["sexo"],
            idade_meses=dados["idade_meses"],
            porte=dados["porte"],
            temperamento=dados["temperamento"],
            data_entrada=dados["data_entrada"],
            independencia=dados["independencia"],
        )
        obj.status = StatusAnimal(dados["status"])
        obj.historico_eventos = dados.get("historico_eventos", [])
        obj.historico_vacinas = dados.get("historico_vacinas", [])
        obj.nivel_adestramento = dados.get("nivel_adestramento", "")
        return obj