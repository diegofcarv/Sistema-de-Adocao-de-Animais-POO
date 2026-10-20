from typing import TYPE_CHECKING
from .base_fee_strategy import BaseFeeStrategy

if TYPE_CHECKING:
    from ..animais.animal import Animal

class SpecialCareFee(BaseFeeStrategy):
    """
    Estratégia de taxa para animais com cuidados especiais.

    Taxa reduzida para incentivar adoção responsável.
    """

    TAXA_REDUZIDA = 50.0

    def calcular_taxa(self, animal: "Animal") -> float:
        """
        Calcula a taxa reduzida para animais com cuidados especiais.

        Args:
            animal (Animal): O animal envolvido na adoção.

        Returns:
            float: Valor da taxa reduzida.
        """
        return self.TAXA_REDUZIDA
