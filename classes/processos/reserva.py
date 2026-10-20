from datetime import datetime, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..animais.animal import Animal
    from ..pessoas.adotante import Adotante
    from ..politicas.politica_reserva import PoliticaReserva

class Reserva:
    """
    Representa o bloqueio temporário de um animal por um adotante interessado.

    Attributes:
        id_reserva (str): Identificador único da reserva.
        animal (Animal): Instância do animal reservado.
        adotante (Adotante): Adotante que solicitou o bloqueio.
        politica_reserva (PoliticaReserva): Regras validadas no ato.
        data_criacao (str): Data e hora da solicitação (ISO 8601).
        status_reserva (str): Estado atual: 'ativa', 'efetivada' ou 'expirada'.
    """

    def __init__(self, id_reserva: str, animal: "Animal", adotante: "Adotante",
                 politica_reserva: "PoliticaReserva", data_criacao: str = None):
        from ..excecoes import ReservaInvalidaError, PoliticaNaoAtendidaError
        from ..status_animal import StatusAnimal

        if animal.status != StatusAnimal.DISPONIVEL:
            raise ReservaInvalidaError(
                f"Animal '{animal.nome}' não está disponível para reserva (status: {animal.status.value})."
            )
        if not politica_reserva.validar_elegibilidade(adotante):
            raise PoliticaNaoAtendidaError(
                f"Adotante '{adotante.nome}' não atende aos critérios de elegibilidade."
            )

        self.id_reserva = id_reserva
        self.animal = animal
        self.adotante = adotante
        self.politica_reserva = politica_reserva
        self.data_criacao = data_criacao or datetime.now().isoformat()
        self.status_reserva = "ativa"

        animal.mudar_status(StatusAnimal.RESERVADO)

    def verificar_expiracao(self) -> bool:
        """
        Compara a data atual com data de criação + duração da política.

        Returns:
            bool: True se a reserva já expirou.
        """
        from ..status_animal import StatusAnimal
        duracao_horas = self.politica_reserva.obter_duracao_reserva()
        data_criacao = datetime.fromisoformat(self.data_criacao)
        data_expiracao = data_criacao + timedelta(hours=duracao_horas)
        expirou = datetime.now() > data_expiracao
        if expirou and self.status_reserva == "ativa":
            self.status_reserva = "expirada"
            self.animal.mudar_status(StatusAnimal.DISPONIVEL)
            self.animal.registrar_evento(f"Reserva {self.id_reserva} expirada automaticamente.")
        return expirou

    def cancelar(self) -> None:
        """Encerra a reserva manualmente e libera o animal para DISPONIVEL."""
        from ..excecoes import ReservaInvalidaError
        from ..status_animal import StatusAnimal

        if self.status_reserva != "ativa":
            raise ReservaInvalidaError(f"Reserva '{self.id_reserva}' não está ativa.")
        self.status_reserva = "cancelada"
        self.animal.mudar_status(StatusAnimal.DISPONIVEL)
        self.animal.registrar_evento(f"Reserva {self.id_reserva} cancelada pelo adotante.")

    def confirmar(self) -> None:
        """Marca a reserva como efetivada (pronta para gerar adoção)."""
        from ..excecoes import ReservaInvalidaError

        if self.status_reserva != "ativa":
            raise ReservaInvalidaError(f"Reserva '{self.id_reserva}' não está ativa.")
        if self.verificar_expiracao():
            raise ReservaInvalidaError(f"Reserva '{self.id_reserva}' já expirou.")
        self.status_reserva = "efetivada"
