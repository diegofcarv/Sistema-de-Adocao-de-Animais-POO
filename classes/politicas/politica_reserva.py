from .politica import Politica

class PoliticaReserva(Politica):
    """Define e valida as políticas relacionadas às reservas temporárias de animais."""

    def validar_elegibilidade(self, adotante) -> bool:
        """
        Verifica se o adotante cumpre os critérios para fazer uma reserva.

        Args:
            adotante (Adotante): O adotante a ser avaliado.

        Returns:
            bool: True se elegível, False caso contrário.
        """
        config = self.carregar_configuracoes()
        idade_minima = config.get("idade_minima_adotante", 18)
        return adotante.idade >= idade_minima

    def obter_duracao_reserva(self) -> int:
        """
        Retorna a duração limite da reserva em horas conforme o settings.json.

        Returns:
            int: Duração da reserva em horas (padrão: 48h).
        """
        config = self.carregar_configuracoes()
        return config.get("duracao_reserva_horas", 48)
