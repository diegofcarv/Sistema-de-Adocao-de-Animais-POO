from typing import TYPE_CHECKING
from .base_fee_strategy import BaseFeeStrategy

if TYPE_CHECKING:
    from ..animais.animal import Animal

class PuppyFee(BaseFeeStrategy):
    """
    Estratégia de taxa para animais filhotes.

    Inclui custos de vacinas e castração primária.
    """

    TAXA_BASE = 150.0
    ADICIONAL_VACINAS = 80.0
    ADICIONAL_CASTRACAO = 120.0

    def calcular_taxa(self, animal: "Animal") -> float:
        """
        Calcula a taxa base acrescida dos custos de vacinas e castração.

        Args:
            animal (Animal): O animal envolvido na adoção.

        Returns:
            float: Valor total da taxa para filhote.
        """
        return round(self.TAXA_BASE + self.ADICIONAL_VACINAS + self.ADICIONAL_CASTRACAO, 2)
