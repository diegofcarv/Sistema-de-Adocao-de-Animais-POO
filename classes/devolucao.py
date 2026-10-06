class Devolucao:
    """
    Registra e processa o retorno de um animal adotado para o sistema.
    
    Attributes:
        id_devolucao (str): Identificador único do retorno.
        adocao (Adocao): Registro da adoção que foi desfeita.
        motivo (str): Razão da devolução informada pelo adotante.
        condicao_animal (str): Parecer clínico e comportamental no retorno.
        data_devolucao (str): Data em que a devolução ocorreu.
        status (str): Status interno do trâmite processual.
    """
    def processar_devolucao(self) -> None:
        """Altera os registros do adotante e converte a adoção em desfeita."""
        pass

    def reavaliar_animal(self) -> None:
        """Encaminha o animal para QUARENTENA ou de volta a DISPONIVEL baseado na condicao_animal."""
        pass