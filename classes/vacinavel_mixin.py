from typing import List

class VacinavelMixin:
    """Fornece comportamentos relacionados à vacinação dos animais."""
    def vacinar(self, vacina: str) -> None:
        """
        Registra uma vacina no histórico.
        
        Args:
            vacina (str): Nome da vacina.
        """
        if not hasattr(self, 'historico_vacinas'):
            self.historico_vacinas: List[str] = []
        self.historico_vacinas.append(vacina)