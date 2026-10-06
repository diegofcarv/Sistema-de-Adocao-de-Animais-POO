class FilaEspera:
    """
    Gerencia a fila de prioridade para adoção de animais disputados.
    
    Attributes:
        animal (Animal): O animal vinculado a esta fila.
        fila (list): Lista de adotantes interessados ordenados por prioridade/tempo.
    """
    def adicionar(self) -> None:
        """Adiciona um adotante à fila de espera."""
        pass

    def remover(self) -> None:
        """Remove um adotante desistente da fila."""
        pass

    def proximo(self):
        """Retorna o adotante com maior prioridade atual."""
        pass

    def notificar_proximo(self) -> None:
        """Emite alerta ao próximo da fila indicando que o animal está liberado."""
        pass

    def __len__(self) -> int:
        """Retorna a quantidade de adotantes registrados na fila."""
        pass