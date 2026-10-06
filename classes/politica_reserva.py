from politica import Politica

class PoliticaReserva(Politica):
    """Define e valida as políticas relacionadas às reservas temporárias de animais."""
    def validar_elegibilidade(self) -> bool:
        """Verifica se o adotante cumpre os critérios (ex: limite de reservas ativas)."""
        pass

    def obter_duracao_reserva(self) -> int:
        """Retorna a duração limite da reserva em horas (ex: 48h)."""
        pass