from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..animais.animal import Animal

class BaseFeeStrategy(ABC):
    """Interface abstrata do padrão Strategy para cálculo de taxas de adoção."""

    @abstractmethod
    def calcular_taxa(self, animal: "Animal") -> float:
        """
        Calcula o valor da taxa de adoção com base nas regras da estratégia.

        Args:
            animal (Animal): O animal envolvido na adoção.

        Returns:
            float: Valor da taxa em reais.
        """
        pass
