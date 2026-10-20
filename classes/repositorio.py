import json
import os
from typing import Any, Dict, List, Optional
from .excecoes import RepositorioError

class Repositorio:
    """
    Gerencia a persistência de dados do sistema em arquivo JSON.

    Attributes:
        caminho_arquivo (str): Caminho para o arquivo JSON de dados.
    """

    def __init__(self, caminho_arquivo: str):
        self.caminho_arquivo = caminho_arquivo
        self._garantir_arquivo()

    def _garantir_arquivo(self) -> None:
        """Cria o arquivo JSON vazio se ele ainda não existir."""
        if not os.path.exists(self.caminho_arquivo):
            diretorio = os.path.dirname(self.caminho_arquivo)
            if diretorio:
                os.makedirs(diretorio, exist_ok=True)
            with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def carregar(self) -> Dict[str, Any]:
        """
        Carrega todos os dados do arquivo JSON para a memória.

        Returns:
            dict: Dados armazenados no arquivo.

        Raises:
            RepositorioError: Se o arquivo não puder ser lido.
        """
        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            raise RepositorioError(f"Erro ao carregar dados de '{self.caminho_arquivo}': {e}")

    def salvar(self, dados: Dict[str, Any]) -> None:
        """
        Persiste o dicionário de dados completo no arquivo JSON.

        Args:
            dados (dict): Dados a serem salvos.

        Raises:
            RepositorioError: Se o arquivo não puder ser escrito.
        """
        try:
            with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)
        except OSError as e:
            raise RepositorioError(f"Erro ao salvar dados em '{self.caminho_arquivo}': {e}")

    def buscar(self, colecao: str, id_campo: str, valor_id: str) -> Optional[Dict]:
        """
        Busca um registro pelo seu identificador dentro de uma coleção.

        Args:
            colecao (str): Nome da coleção (ex: 'animais', 'adotantes').
            id_campo (str): Nome do campo identificador (ex: 'id_animal').
            valor_id (str): Valor do identificador a buscar.

        Returns:
            dict | None: Registro encontrado ou None.
        """
        dados = self.carregar()
        for registro in dados.get(colecao, []):
            if registro.get(id_campo) == valor_id:
                return registro
        return None

    def inserir(self, colecao: str, registro: Dict) -> None:
        """
        Adiciona um novo registro em uma coleção.

        Args:
            colecao (str): Nome da coleção.
            registro (dict): Dados do novo registro.
        """
        dados = self.carregar()
        if colecao not in dados:
            dados[colecao] = []
        dados[colecao].append(registro)
        self.salvar(dados)

    def atualizar(self, colecao: str, id_campo: str, valor_id: str, novos_dados: Dict) -> bool:
        """
        Atualiza um registro existente em uma coleção.

        Args:
            colecao (str): Nome da coleção.
            id_campo (str): Campo identificador.
            valor_id (str): Valor do identificador.
            novos_dados (dict): Campos a serem atualizados.

        Returns:
            bool: True se o registro foi encontrado e atualizado.
        """
        dados = self.carregar()
        for registro in dados.get(colecao, []):
            if registro.get(id_campo) == valor_id:
                registro.update(novos_dados)
                self.salvar(dados)
                return True
        return False

    def deletar(self, colecao: str, id_campo: str, valor_id: str) -> bool:
        """
        Remove um registro de uma coleção pelo identificador.

        Args:
            colecao (str): Nome da coleção.
            id_campo (str): Campo identificador.
            valor_id (str): Valor do identificador.

        Returns:
            bool: True se o registro foi encontrado e removido.
        """
        dados = self.carregar()
        lista = dados.get(colecao, [])
        nova_lista = [r for r in lista if r.get(id_campo) != valor_id]
        if len(nova_lista) == len(lista):
            return False
        dados[colecao] = nova_lista
        self.salvar(dados)
        return True

    def listar(self, colecao: str) -> List[Dict]:
        """
        Retorna todos os registros de uma coleção.

        Args:
            colecao (str): Nome da coleção.

        Returns:
            list: Lista de registros.
        """
        dados = self.carregar()
        return dados.get(colecao, [])
