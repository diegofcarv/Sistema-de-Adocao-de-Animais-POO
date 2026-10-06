class Adocao:
    """
    Registra a efetivação do processo de adoção, gerando vínculo permanente.
    
    Attributes:
        id_adocao (str): Identificador único.
        reserva (Reserva): Dados da reserva que deu origem ao processo.
        politica_adocao (PoliticaAdocao): Regras utilizadas para validação final.
        taxa (BaseFeeStrategy): Estratégia de taxa aplicada no processo.
        contrato (str): Texto legal gerado e aceito pelas partes.
        data_adocao (str): Data de conclusão do processo.
    """
    def efetivar(self) -> None:
        """Executa a transição de status do animal e fecha a transação."""
        pass

    def gerar_contrato(self) -> str:
        """Monta o arquivo de texto contendo resumo do adotante, animal e taxas."""
        pass