from .politica import Politica

class PoliticaQuarentena(Politica):
    """Define os critérios de saúde/comportamento e duração mínima para isolamento."""

    DURACAO_MINIMA_DIAS = 14

    def obter_duracao_quarentena(self) -> int:
        """
        Retorna a duração mínima da quarentena em dias.

        Returns:
            int: Número de dias de quarentena (padrão: 14).
        """
        return self.DURACAO_MINIMA_DIAS

    def exige_quarentena(self, condicao_animal: str) -> bool:
        """
        Determina se a condição relatada exige quarentena.

        Args:
            condicao_animal (str): Condição clínica/comportamental do animal devolvido.

        Returns:
            bool: True se a condição exige quarentena.
        """
        condicoes_quarentena = {"doente", "agressivo", "lesionado", "estressado"}
        return condicao_animal.lower() in condicoes_quarentena
