from abc import ABC

class Pessoa(ABC):
    """Classe abstrata que representa uma pessoa no sistema."""
    def __init__(self, cpf: str, nome: str, idade: int, telefone: str, email: str):
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.idade = idade

    @property
    def idade(self) -> int:
        """int: Idade da pessoa."""
        return self._idade

    @idade.setter
    def idade(self, valor: int) -> None:
        if valor < 0:
            raise ValueError("A idade da pessoa não pode ser negativa.")
        self._idade = valor