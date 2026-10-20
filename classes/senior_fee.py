from typing import TYPE_CHECKING
from .base_fee_strategy import BaseFeeStrategy

if TYPE_CHECKING:
    from .animal import Animal

class SeniorFee(BaseFeeStrategy):
    """
    Estratégia de taxa para animais idosos (sênior).

    Aplica desconto financeiro para incentivar a adoção de animais mais velhos.
    Animais com mais de 84 meses (7 anos) são considerados sênior.
    """

    TAXA_BASE = 150.0
    DESCONTO_SENIOR = 0.50  # 50% de desconto

    def calcular_taxa(self, animal: "Animal") -> float:
        """
        Calcula a taxa com desconto de 50% para animais sênior.

        Args:
            animal (Animal): O animal envolvido na adoção.

        Returns:
            float: Valor da taxa com desconto aplicado.
        """
        return round(self.TAXA_BASE * (1 - self.DESCONTO_SENIOR), 2)
