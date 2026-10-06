from base_fee_strategy import BaseFeeStrategy

class SpecialCareFee(BaseFeeStrategy):
    """
    Estratégia de taxa para animais que necessitam de cuidados especiais.
    Pode isentar taxas ou aplicar custos específicos dependendo da política da ONG.
    """
    def calcular_taxa(self) -> float:
        pass