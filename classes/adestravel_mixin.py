class AdestravelMixin:
    """Fornece comportamentos relacionados ao adestramento dos animais."""
    def treinar(self, comando: str) -> None:
        """
        Registra um novo comando ensinado ao animal.
        
        Args:
            comando (str): O comando ensinado.
        """
        self.nivel_adestramento = f"Sabe o comando: {comando}"