from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..animais.animal import Animal
    from ..pessoas.adotante import Adotante

class _EntradaFila:
    """Representa uma entrada na fila com adotante, pontuação e momento de entrada."""

    def __init__(self, adotante: "Adotante", pontuacao: float, data_entrada: str):
        self.adotante = adotante
        self.pontuacao = pontuacao
        self.data_entrada = data_entrada

    def __lt__(self, outro: "_EntradaFila") -> bool:
        """Ordena por pontuação decrescente; em empate, por data de entrada crescente."""
        if self.pontuacao != outro.pontuacao:
            return self.pontuacao > outro.pontuacao
        return self.data_entrada < outro.data_entrada


class FilaEspera:
    """
    Gerencia a fila de prioridade para adoção de animais disputados.

    Attributes:
        animal (Animal): O animal vinculado a esta fila.
        fila (list): Lista de entradas ordenadas por pontuação e tempo de espera.
    """

    def __init__(self, animal: "Animal"):
        self.animal = animal
        self.fila: List[_EntradaFila] = []

    def adicionar(self, adotante: "Adotante", data_entrada: str = None) -> None:
        """
        Adiciona um adotante à fila com sua pontuação de compatibilidade.

        Args:
            adotante (Adotante): O adotante interessado.
            data_entrada (str): Momento de entrada na fila (ISO 8601). Usa agora se omitido.
        """
        from datetime import datetime
        data = data_entrada or datetime.now().isoformat()
        pontuacao = adotante.calcular_pontuacao_compatibilidade(self.animal)
        entrada = _EntradaFila(adotante, pontuacao, data)
        self.fila.append(entrada)
        self.fila.sort()

    def remover(self, adotante: "Adotante") -> bool:
        """
        Remove um adotante desistente da fila.

        Args:
            adotante (Adotante): O adotante a ser removido.

        Returns:
            bool: True se encontrado e removido.
        """
        for entrada in self.fila:
            if entrada.adotante.cpf == adotante.cpf:
                self.fila.remove(entrada)
                return True
        return False

    def proximo(self) -> Optional["Adotante"]:
        """
        Retorna o adotante com maior prioridade sem removê-lo da fila.

        Returns:
            Adotante | None: Próximo da fila ou None se vazia.
        """
        if not self.fila:
            return None
        return self.fila[0].adotante

    def notificar_proximo(self) -> None:
        """Emite um evento ao próximo da fila indicando que o animal está liberado."""
        proximo = self.proximo()
        if proximo:
            self.animal.registrar_evento(
                f"Fila de espera: '{proximo.nome}' notificado — {self.animal.nome} está disponível."
            )

    def __len__(self) -> int:
        """Retorna a quantidade de adotantes registrados na fila."""
        return len(self.fila)

    def __lt__(self, outro: "FilaEspera") -> bool:
        """Compara filas pelo tamanho (mais disputado = maior)."""
        return len(self) > len(outro)
