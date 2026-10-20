import json
import os
from abc import ABC

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'settings.json')

class Politica(ABC):
    """
    Classe base abstrata para as políticas de regras de negócio do sistema.

    Attributes:
        settings_file (str): Caminho para o arquivo settings.json.
    """

    def __init__(self, settings_file: str = SETTINGS_PATH):
        self.settings_file = settings_file

    def carregar_configuracoes(self) -> dict:
        """
        Lê e retorna as configurações definidas no arquivo JSON de settings.

        Returns:
            dict: Dicionário com as configurações do sistema.

        Raises:
            RepositorioError: Se o arquivo não for encontrado ou estiver malformado.
        """
        from ..excecoes import RepositorioError
        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise RepositorioError(f"Arquivo de configurações não encontrado: {self.settings_file}")
        except json.JSONDecodeError as e:
            raise RepositorioError(f"Erro ao ler o arquivo de configurações: {e}")
