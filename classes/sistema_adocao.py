# classes/sistema_adocao.py
import json
import os
from datetime import datetime
from typing import List, Optional

from .animais import Cachorro, Gato, animal_de_dict
from .pessoas import Adotante
from .politicas import PoliticaReserva, PoliticaAdocao, PoliticaDevolucao, PoliticaQuarentena
from .processos import Reserva, Adocao, Devolucao
from .infra import Repositorio, FilaEspera
from .taxas import SeniorFee, PuppyFee, SpecialCareFee
from .excecoes import ReservaInvalidaError, PoliticaNaoAtendidaError, RepositorioError
from .status_animal import StatusAnimal

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
ANIMAIS_PATH = os.path.join(DATA_DIR, 'animais.json')
ADOTANTES_PATH = os.path.join(DATA_DIR, 'adotantes.json')
SETTINGS_PATH = os.path.join(os.path.dirname(__file__), '..', 'settings.json')


def _carregar_settings() -> dict:
    try:
        with open(SETTINGS_PATH, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


class SistemaAdocao:
    """
    Coordena os fluxos principais do sistema de adoção.
    Atua como Controlador (Controller) recebendo dados e retornando mensagens/resultados.
    """

    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self._repo_animais = Repositorio(ANIMAIS_PATH)
        self._repo_adotantes = Repositorio(ADOTANTES_PATH)

    # ── animais ──────────────────────────────────────────────

    def cadastrar_animal(self, dados: dict) -> str:
        """Cadastra um novo animal no sistema e retorna mensagem de sucesso."""
        especie = dados.get('especie', '').lower()
        if especie == 'cachorro':
            animal = Cachorro(
                id_animal=dados['id_animal'],
                raca=dados['raca'],
                nome=dados['nome'],
                sexo=dados['sexo'],
                idade_meses=int(dados['idade_meses']),
                porte=dados['porte'],
                temperamento=dados.get('temperamento', []),
                data_entrada=dados.get('data_entrada') or datetime.now().strftime('%Y-%m-%d'),
                necessidade_passeio=dados.get('necessidade_passeio', 'media'),
            )
        elif especie == 'gato':
            animal = Gato(
                id_animal=dados['id_animal'],
                raca=dados['raca'],
                nome=dados['nome'],
                sexo=dados['sexo'],
                idade_meses=int(dados['idade_meses']),
                porte=dados['porte'],
                temperamento=dados.get('temperamento', []),
                data_entrada=dados.get('data_entrada') or datetime.now().strftime('%Y-%m-%d'),
                independencia=dados.get('independencia', 'media'),
            )
        else:
            raise ValueError(f"Espécie inválida: '{especie}'. Use 'cachorro' ou 'gato'.")

        existente = self._repo_animais.buscar('animais', 'id_animal', animal.id_animal)
        if existente:
            raise ValueError(f"Já existe um animal com o ID '{animal.id_animal}'.")

        self._repo_animais.inserir('animais', animal.para_dict())
        return f"Animal '{animal.nome}' cadastrado com sucesso."

    def listar_animais(self, status: str = None) -> List[dict]:
        animais = self._repo_animais.listar('animais')
        if status:
            animais = [a for a in animais if a['status'].upper() == status.upper()]
        return animais

    def buscar_animal(self, id_animal: str) -> dict:
        dados = self._repo_animais.buscar('animais', 'id_animal', id_animal)
        if not dados:
            raise ValueError(f"Animal '{id_animal}' não encontrado.")
        return dados

    # ── adotantes ────────────────────────────────────────────

    def cadastrar_adotante(self, dados: dict) -> str:
        """Cadastra um novo adotante e retorna mensagem de sucesso."""
        adotante = Adotante(
            cpf=dados['cpf'],
            nome=dados['nome'],
            idade=int(dados['idade']),
            telefone=dados['telefone'],
            email=dados['email'],
            moradia=dados['moradia'],
            area_util=float(dados['area_util']),
            experiencia_pets=dados.get('experiencia_pets', False),
            criancas=dados.get('criancas', {}),
            outros_animais=dados.get('outros_animais', {}),
            experiencia_anterior=dados.get('experiencia_anterior', {}),
        )

        existente = self._repo_adotantes.buscar('adotantes', 'cpf', adotante.cpf)
        if existente:
            raise ValueError(f"Já existe um adotante com o CPF '{adotante.cpf}'.")

        self._repo_adotantes.inserir('adotantes', adotante.para_dict())
        return f"Adotante '{adotante.nome}' cadastrado com sucesso."

    def listar_adotantes(self) -> List[dict]:
        return self._repo_adotantes.listar('adotantes')

    def buscar_adotante(self, cpf: str) -> dict:
        dados = self._repo_adotantes.buscar('adotantes', 'cpf', cpf)
        if not dados:
            raise ValueError(f"Adotante '{cpf}' não encontrado.")
        return dados

    # ── fluxo de adoção ──────────────────────────────────────

    def reservar(self, id_animal: str, cpf_adotante: str) -> str:
        dados_animal = self.buscar_animal(id_animal)
        dados_adotante = self.buscar_adotante(cpf_adotante)

        animal = animal_de_dict(dados_animal)
        adotante = Adotante.de_dict(dados_adotante)

        politica = PoliticaReserva()
        id_reserva = f"R{datetime.now().strftime('%Y%m%d%H%M%S')}"
        reserva = Reserva(id_reserva, animal, adotante, politica)

        self._repo_animais.atualizar('animais', 'id_animal', id_animal, animal.para_dict())
        return f"Reserva '{id_reserva}' criada com sucesso para '{animal.nome}'."

    def adotar(self, id_animal: str, cpf_adotante: str) -> str:
        """Efetiva adoção e retorna o contrato em formato de string."""
        dados_animal = self.buscar_animal(id_animal)
        dados_adotante = self.buscar_adotante(cpf_adotante)

        animal = animal_de_dict(dados_animal)
        adotante = Adotante.de_dict(dados_adotante)

        if animal.status != StatusAnimal.RESERVADO:
            raise ReservaInvalidaError(f"Animal '{animal.nome}' não está reservado.")

        politica_reserva = PoliticaReserva()
        reserva = Reserva.__new__(Reserva)
        reserva.id_reserva = f"R-{id_animal}"
        reserva.animal = animal
        reserva.adotante = adotante
        reserva.politica_reserva = politica_reserva
        reserva.data_criacao = datetime.now().isoformat()
        reserva.status_reserva = "efetivada"

        taxa = self._escolher_taxa(animal)
        politica_adocao = PoliticaAdocao()
        id_adocao = f"A{datetime.now().strftime('%Y%m%d%H%M%S')}"
        adocao = Adocao(id_adocao, reserva, politica_adocao, taxa)
        adocao.efetivar()

        self._repo_animais.atualizar('animais', 'id_animal', id_animal, animal.para_dict())
        return adocao.contrato

    def devolver(self, id_animal: str, motivo: str, condicao: str) -> str:
        """Registra a devolução e retorna o novo status do animal."""
        dados_animal = self.buscar_animal(id_animal)
        animal = animal_de_dict(dados_animal)

        if animal.status != StatusAnimal.ADOTADO:
            raise ReservaInvalidaError(f"Animal '{animal.nome}' não está adotado.")

        reserva = Reserva.__new__(Reserva)
        reserva.animal = animal

        adocao = Adocao.__new__(Adocao)
        adocao.reserva = reserva

        politica_dev = PoliticaDevolucao()
        politica_qua = PoliticaQuarentena()

        if not politica_dev.validar_motivo(motivo):
            motivos = ', '.join(politica_dev.MOTIVOS_VALIDOS)
            raise ValueError(f"Motivo inválido. Use um dos seguintes: {motivos}")

        id_dev = f"D{datetime.now().strftime('%Y%m%d%H%M%S')}"
        devolucao = Devolucao(id_dev, adocao, motivo, condicao, politica_dev, politica_qua)
        devolucao.processar_devolucao()

        self._repo_animais.atualizar('animais', 'id_animal', id_animal, animal.para_dict())
        return f"Devolução registrada. Status do animal '{animal.nome}' atualizado para: {animal.status.value}."

    def compatibilidade(self, cpf_adotante: str) -> List[tuple]:
        dados_adotante = self.buscar_adotante(cpf_adotante)
        adotante = Adotante.de_dict(dados_adotante)

        disponiveis = self.listar_animais(status='DISPONIVEL')
        resultado = []
        for d in disponiveis:
            animal = animal_de_dict(d)
            score = adotante.calcular_pontuacao_compatibilidade(animal)
            resultado.append((d, score))

        resultado.sort(key=lambda x: x[1], reverse=True)
        return resultado

    # ── utilitário ───────────────────────────────────────────

    def _escolher_taxa(self, animal):
        settings = _carregar_settings()
        limite_filhote = settings.get('limite_filhote_meses', 12)
        limite_senior = settings.get('limite_senior_meses', 84)

        if animal.idade_meses <= limite_filhote:
            return PuppyFee()
        elif animal.idade_meses >= limite_senior:
            return SeniorFee()
        else:
            return SpecialCareFee()