from base_fee_strategy import BaseFeeStrategy

class PuppyFee(BaseFeeStrategy):
    """
    Estratégia de taxa aplicada a animais filhotes.
    Geralmente inclui no cálculo os custos embutidos de vacinas e castração primária.
    """
    def calcular_taxa(self) -> float:
        pass