from base_fee_strategy import BaseFeeStrategy

class SeniorFee(BaseFeeStrategy):
    """
    Estratégia de taxa aplicada a animais idosos (Sênior).
    Aplica desconto financeiro para incentivar a adoção de animais mais velhos.
    """
    def calcular_taxa(self) -> float:
        pass