from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .reserva import Reserva
    from .politica_adocao import PoliticaAdocao
    from .base_fee_strategy import BaseFeeStrategy

class Adocao:
    """
    Registra a efetivação do processo de adoção, gerando vínculo permanente.

    Attributes:
        id_adocao (str): Identificador único.
        reserva (Reserva): Dados da reserva que deu origem ao processo.
        politica_adocao (PoliticaAdocao): Regras utilizadas para validação final.
        taxa (BaseFeeStrategy): Estratégia de taxa aplicada no processo.
        contrato (str): Texto legal gerado e aceito pelas partes.
        data_adocao (str): Data de conclusão do processo (ISO 8601).
    """

    def __init__(self, id_adocao: str, reserva: "Reserva",
                 politica_adocao: "PoliticaAdocao", taxa: "BaseFeeStrategy"):
        self.id_adocao = id_adocao
        self.reserva = reserva
        self.politica_adocao = politica_adocao
        self.taxa = taxa
        self.contrato: str = ""
        self.data_adocao: str = ""

    def efetivar(self) -> None:
        """
        Executa a validação final, altera o status do animal para ADOTADO
        e registra a data da adoção.

        Raises:
            PoliticaNaoAtendidaError: Se as regras de adoção não forem atendidas.
            ReservaInvalidaError: Se a reserva não estiver efetivada.
        """
        from .excecoes import PoliticaNaoAtendidaError, ReservaInvalidaError
        from .status_animal import StatusAnimal

        if self.reserva.status_reserva != "efetivada":
            raise ReservaInvalidaError("A reserva precisa estar efetivada antes de concluir a adoção.")

        adotante = self.reserva.adotante
        animal = self.reserva.animal

        if not self.politica_adocao.validar_idade_minima(adotante):
            raise PoliticaNaoAtendidaError(
                f"Adotante '{adotante.nome}' não possui a idade mínima exigida."
            )
        if not self.politica_adocao.validar_moradia_porte(adotante, animal):
            raise PoliticaNaoAtendidaError(
                f"A moradia de '{adotante.nome}' não é compatível com o porte '{animal.porte}' do animal."
            )

        self.data_adocao = datetime.now().isoformat()
        animal.mudar_status(StatusAnimal.ADOTADO)
        animal.registrar_evento(f"Adotado por {adotante.nome} em {self.data_adocao[:10]}.")
        self.contrato = self.gerar_contrato()

    def gerar_contrato(self) -> str:
        """
        Monta o texto do contrato com resumo do adotante, animal e taxa.

        Returns:
            str: Texto completo do contrato de adoção.
        """
        animal = self.reserva.animal
        adotante = self.reserva.adotante
        valor_taxa = self.taxa.calcular_taxa(animal)

        contrato = (
            f"====== CONTRATO DE ADOÇÃO ======\n"
            f"ID da Adoção  : {self.id_adocao}\n"
            f"Data          : {self.data_adocao[:10] if self.data_adocao else 'N/A'}\n\n"
            f"--- ANIMAL ---\n"
            f"Nome          : {animal.nome}\n"
            f"Espécie       : {getattr(animal, 'especie', 'N/A')}\n"
            f"Raça          : {animal.raca}\n"
            f"Porte         : {animal.porte}\n"
            f"Idade         : {animal.idade_meses} meses\n\n"
            f"--- ADOTANTE ---\n"
            f"Nome          : {adotante.nome}\n"
            f"CPF           : {adotante.cpf}\n"
            f"Moradia       : {adotante.moradia} ({adotante.area_util} m²)\n\n"
            f"--- TAXA ---\n"
            f"Valor         : R$ {valor_taxa:.2f}\n"
            f"Estratégia    : {type(self.taxa).__name__}\n\n"
            f"Ao assinar este contrato, o adotante compromete-se a fornecer\n"
            f"cuidados adequados ao animal pelo resto de sua vida.\n"
            f"================================\n"
        )
        return contrato
