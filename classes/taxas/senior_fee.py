from typing import TYPE_CHECKING
from .base_fee_strategy import BaseFeeStrategy

if TYPE_CHECKING:
    from ..animais.animal import Animal

class SeniorFee(BaseFeeStrategy):
    """
    Estratégia de taxa para animais idosos (sênior).

    Aplica desconto de 50% para incentivar a adoção de animais mais velhos.
    """

    TAXA_BASE = 150.0
    DESCONTO_SENIOR = 0.50

    def calcular_taxa(self, animal: "Animal") -> float:
        """
        Calcula a taxa com desconto de 50% para animais sênior.

        Args:
            animal (Animal): O animal envolvido na adoção.

        Returns:
            float: Valor da taxa com desconto aplicado.
        """
        return round(self.TAXA_BASE * (1 - self.DESCONTO_SENIOR), 2)
