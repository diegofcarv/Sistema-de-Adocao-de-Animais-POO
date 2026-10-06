from abc import ABC

class Politica(ABC):
    """
    Classe base abstrata para as políticas de regras de negócio do sistema.
    
    Attributes:
        settings_file (str): Caminho para o arquivo settings.json.
    """
    def carregar_configuracoes(self) -> dict:
        """Lê e retorna as configurações definidas no arquivo JSON de settings."""
        pass