from typing import TYPE_CHECKING
from .base_fee_strategy import BaseFeeStrategy

if TYPE_CHECKING:
    from .animal import Animal

class SpecialCareFee(BaseFeeStrategy):
    """
    Estratégia de taxa para animais com cuidados especiais.

    Pode isentar a taxa ou aplicar custos específicos dependendo da
    política da ONG. Animais com necessidades especiais têm taxa reduzida
    para incentivar adoção responsável.
    """

    TAXA_ISENCAO = 0.0
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
