from enum import Enum

class StatusAnimal(Enum):
    """Enumeração dos estados possíveis de um animal no sistema."""
    DISPONIVEL = "DISPONIVEL"
    RESERVADO = "RESERVADO"
    ADOTADO = "ADOTADO"
    DEVOLVIDO = "DEVOLVIDO"
    QUARENTENA = "QUARENTENA"
    INADOTAVEL = "INADOTAVEL"