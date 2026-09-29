from abc import ABC
from enum import Enum

class StatusAnimal(Enum):
    """
    Enumeração dos estados possíveis de um animal no sistema.
    """
    DISPONIVEL = "DISPONIVEL"
    RESERVADO = "RESERVADO"
    ADOTADO = "ADOTADO"
    DEVOLVIDO = "DEVOLVIDO"
    QUARENTENA = "QUARENTENA"
    INADOTAVEL = "INADOTAVEL"

class VacinavelMixin:
    """
    Fornece comportamentos relacionados à vacinação dos animais.
    """
    pass

class AdestravelMixin:
    """
    Fornece comportamentos relacionados ao adestramento dos animais.
    """
    pass

class Animal(ABC, VacinavelMixin, AdestravelMixin):
    """
    Classe abstrata que representa um animal do sistema.
    
    Attributes:
        especie (str): A espécie do animal.
        status (StatusAnimal): O estado atual do animal no sistema.
    """
    pass

class Cachorro(Animal):
    """
    Representa um cachorro disponível para adoção.
    """
    pass

class Gato(Animal):
    """
    Representa um gato disponível para adoção.
    """
    pass

class Pessoa(ABC):
    """
    Classe abstrata que representa uma pessoa do sistema.
    """
    pass

class Adotante(Pessoa):
    """
    Representa uma pessoa interessada em adotar um animal.
    """
    pass

class BaseFeeStrategy(ABC):
    """
    Define a estrutura básica para as estratégias de cálculo de taxa.
    """
    pass

class SeniorFee(BaseFeeStrategy):
    """
    Representa a estratégia de taxa para animais idosos.
    """
    pass

class PuppyFee(BaseFeeStrategy):
    """
    Representa a estratégia de taxa para animais filhotes.
    """
    pass

class SpecialCareFee(BaseFeeStrategy):
    """
    Representa a estratégia de taxa para animais que necessitam de cuidados especiais.
    """
    pass

class Politica(ABC):
    """
    Classe base abstrata para as políticas utilizadas pelo sistema.
    """
    pass

class PoliticaReserva(Politica):
    """
    Define as políticas relacionadas às reservas.
    """
    pass

class PoliticaAdocao(Politica):
    """
    Define as políticas relacionadas às adoções.
    """
    pass

class PoliticaDevolucao(Politica):
    """
    Define as políticas relacionadas às devoluções.
    """
    pass

class PoliticaQuarentena(Politica):
    """
    Define as políticas relacionadas à quarentena dos animais.
    """
    pass

class Repositorio:
    """
    Responsável pela persistência dos dados do sistema.
    """
    pass

class FilaEspera:
    """
    Representa a fila de espera para adoção de um animal.
    """
    pass

class Reserva:
    """
    Representa a reserva temporária de um animal por um adotante.
    """
    pass

class Adocao:
    """
    Representa a efetivação de uma adoção, gerando o contrato.
    """
    pass

class Devolucao:
    """
    Representa a devolução de um animal após uma adoção.
    """
    pass