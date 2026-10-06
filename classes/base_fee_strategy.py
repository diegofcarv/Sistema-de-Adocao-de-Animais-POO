from abc import ABC, abstractmethod

class BaseFeeStrategy(ABC):
    """
    Interface abstrata do padrão Strategy para cálculo de taxas de adoção.
    """
    @abstractmethod
    def calcular_taxa(self) -> float:
        """Calcula o valor da taxa de adoção com base nas regras da estratégia."""
        pass