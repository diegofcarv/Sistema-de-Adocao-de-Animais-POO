from .politica import Politica

class PoliticaDevolucao(Politica):
    """Define os motivos válidos, penalidades e prazos para a devolução de um animal."""

    MOTIVOS_VALIDOS = [
        "incompatibilidade_comportamental",
        "problema_saude_animal",
        "problema_saude_adotante",
        "mudanca_moradia",
        "incompatibilidade_outros_animais",
        "outros",
    ]

    def validar_motivo(self, motivo: str) -> bool:
        """
        Verifica se o motivo da devolução é reconhecido pelo sistema.

        Args:
            motivo (str): Motivo informado pelo adotante.

        Returns:
            bool: True se o motivo for válido.
        """
        return motivo in self.MOTIVOS_VALIDOS
