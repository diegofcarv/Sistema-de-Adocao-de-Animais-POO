class Reserva:
    """
    Representa o bloqueio temporário de um animal por um adotante interessado.
    
    Attributes:
        id_reserva (str): Identificador único da reserva.
        animal (Animal): Instância do animal reservado.
        adotante (Adotante): Adotante que solicitou o bloqueio.
        politica_reserva (PoliticaReserva): Regras validadas no ato.
        data_criacao (str): Data e hora da solicitação.
        status_reserva (str): Estado atual (ativa, efetivada, expirada).
    """
    def verificar_expiracao(self) -> bool:
        """Compara a data atual com a data de criação + duração da política."""
        pass

    def cancelar(self) -> None:
        """Encerra a reserva manualmente e libera o animal."""
        pass

    def confirmar(self) -> None:
        """Converte a reserva em um processo ativo de adoção."""
        pass