from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .adocao import Adocao
    from ..politicas.politica_devolucao import PoliticaDevolucao
    from ..politicas.politica_quarentena import PoliticaQuarentena

class Devolucao:
    """
    Registra e processa o retorno de um animal adotado para o sistema.

    Attributes:
        id_devolucao (str): Identificador único do retorno.
        adocao (Adocao): Registro da adoção que foi desfeita.
        motivo (str): Razão da devolução informada pelo adotante.
        condicao_animal (str): Parecer clínico e comportamental no retorno.
        data_devolucao (str): Data em que a devolução ocorreu (ISO 8601).
        status (str): Status interno do trâmite ('pendente', 'processada').
    """

    def __init__(self, id_devolucao: str, adocao: "Adocao", motivo: str,
                 condicao_animal: str, politica_devolucao: "PoliticaDevolucao",
                 politica_quarentena: "PoliticaQuarentena"):
        self.id_devolucao = id_devolucao
        self.adocao = adocao
        self.motivo = motivo
        self.condicao_animal = condicao_animal
        self.politica_devolucao = politica_devolucao
        self.politica_quarentena = politica_quarentena
        self.data_devolucao = datetime.now().isoformat()
        self.status = "pendente"

    def processar_devolucao(self) -> None:
        """
        Altera o status do animal para DEVOLVIDO e registra o evento.

        Raises:
            ReservaInvalidaError: Se o animal não estiver com status ADOTADO.
        """
        from ..status_animal import StatusAnimal
        from ..excecoes import ReservaInvalidaError

        animal = self.adocao.reserva.animal
        if animal.status != StatusAnimal.ADOTADO:
            raise ReservaInvalidaError("Só é possível devolver um animal com status ADOTADO.")

        animal.mudar_status(StatusAnimal.DEVOLVIDO)
        animal.registrar_evento(
            f"Devolvido em {self.data_devolucao[:10]}. Motivo: {self.motivo}."
        )
        self.status = "processada"
        self.reavaliar_animal()

    def reavaliar_animal(self) -> None:
        """
        Encaminha o animal para QUARENTENA ou de volta a DISPONIVEL
        com base na condição relatada.
        """
        from ..status_animal import StatusAnimal

        animal = self.adocao.reserva.animal
        if self.politica_quarentena.exige_quarentena(self.condicao_animal):
            animal.mudar_status(StatusAnimal.QUARENTENA)
            animal.registrar_evento(
                f"Encaminhado para quarentena. Condição: {self.condicao_animal}."
            )
        else:
            animal.mudar_status(StatusAnimal.DISPONIVEL)
            animal.registrar_evento("Reavaliado e disponibilizado novamente para adoção.")
