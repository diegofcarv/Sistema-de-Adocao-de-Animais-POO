import pytest
from classes.status_animal import StatusAnimal
from classes.animais import Cachorro, Gato
from classes.pessoas import Adotante
from classes.excecoes import (
    ReservaInvalidaError,
    TransicaoDeEstadoInvalidaError,
    PoliticaNaoAtendidaError,
)


# ──────────────────────────────────────────────
# Fixtures reutilizáveis
# ──────────────────────────────────────────────

@pytest.fixture
def cachorro_basico():
    return Cachorro("C001", "Vira-lata", "Rex", "M", 24, "M", ["Brincalhão"], "2026-10-01", "Alta")

@pytest.fixture
def gato_basico():
    return Gato("G001", "Siamês", "Mia", "F", 12, "P", ["Calma"], "2026-10-02", "Alta")

@pytest.fixture
def adotante_basico():
    return Adotante(
        cpf="123.456.789-00", nome="Diêgo", idade=20, telefone="88999999999",
        email="diego@email.com", moradia="casa", area_util=150.0,
        experiencia_pets=True, criancas={}, outros_animais={},
        experiencia_anterior={"quantidade": 2}
    )

@pytest.fixture
def adotante_menor():
    return Adotante(
        cpf="000.000.000-00", nome="Menor", idade=16, telefone="88000000000",
        email="menor@email.com", moradia="casa", area_util=100.0,
        experiencia_pets=False, criancas={}, outros_animais={},
        experiencia_anterior={}
    )


# ──────────────────────────────────────────────
# Entrega 2 — classes base e encapsulamento
# ──────────────────────────────────────────────

def test_criacao_cachorro(cachorro_basico):
    """Testa a criação de um cachorro e herança de atributos."""
    dog = cachorro_basico
    assert dog.nome == "Rex"
    assert dog.especie == "cachorro"
    assert dog.porte == "M"
    assert dog.status == StatusAnimal.DISPONIVEL

def test_encapsulamento_porte_animal_invalido():
    """Testa se o @property impede porte inválido."""
    with pytest.raises(ValueError, match="O porte deve ser obrigatoriamente 'P', 'M' ou 'G'."):
        Gato("G001", "Siamês", "Mia", "F", 12, "X", ["Calma"], "2026-10-02", "Alta")

def test_encapsulamento_idade_negativa():
    """Testa se o @property impede idades negativas."""
    with pytest.raises(ValueError, match="A idade do animal não pode ser negativa."):
        Cachorro("C002", "Poodle", "Bidu", "M", -5, "P", [], "2026-10-05", "Média")

def test_metodos_especiais_animal(cachorro_basico):
    """Testa os métodos __eq__, __str__ e __iter__."""
    dog1 = cachorro_basico
    dog2 = Cachorro("C001", "Vira-lata", "Rex", "M", 24, "M", ["Brincalhão"], "2026-10-01", "Alta")

    assert dog1 == dog2
    assert "Rex (cachorro - Vira-lata)" in str(dog1)

    dog1.registrar_evento("Chegou ao abrigo")
    dog1.vacinar("Raiva")

    historico = list(dog1)
    assert len(historico) == 1
    assert historico[0] == "Chegou ao abrigo"

def test_criacao_adotante_e_moradia(adotante_basico):
    """Testa a criação do adotante e a validação da propriedade moradia."""
    adotante = adotante_basico
    assert adotante.nome == "Diêgo"
    assert adotante.moradia == "casa"

    with pytest.raises(ValueError):
        adotante.moradia = "fazenda"


# ──────────────────────────────────────────────
# Entrega 3 — herança, relações e persistência
# ──────────────────────────────────────────────

def test_ordenacao_por_data_entrada():
    """Testa __lt__: animal mais antigo vem primeiro."""
    dog_antigo = Cachorro("C010", "Poodle", "Bolinha", "M", 6, "P", [], "2026-01-01", "Baixa")
    dog_novo   = Cachorro("C011", "Labrador", "Thor", "M", 12, "G", [], "2026-09-01", "Alta")
    assert dog_antigo < dog_novo

def test_transicao_estado_valida(cachorro_basico):
    """Testa que uma transição permitida é executada sem erro."""
    dog = cachorro_basico
    assert dog.status == StatusAnimal.DISPONIVEL
    dog.mudar_status(StatusAnimal.INADOTAVEL)
    assert dog.status == StatusAnimal.INADOTAVEL

def test_transicao_estado_invalida(cachorro_basico):
    """Testa que uma transição proibida levanta TransicaoDeEstadoInvalidaError."""
    dog = cachorro_basico
    with pytest.raises(TransicaoDeEstadoInvalidaError):
        dog.mudar_status(StatusAnimal.ADOTADO)

def test_compatibilidade_alta(adotante_basico, cachorro_basico):
    """Adotante experiente em casa grande deve ter pontuação alta com animal médio."""
    score = adotante_basico.calcular_pontuacao_compatibilidade(cachorro_basico)
    assert score >= 70

def test_compatibilidade_baixa_porte_g_no_apto():
    """Adotante em apartamento pequeno deve ter pontuação baixa com animal grande."""
    adotante = Adotante(
        "111.111.111-11", "João", 25, "88111111111", "joao@email.com",
        "apto", 40.0, False, {}, {}, {}
    )
    cachorro_g = Cachorro("C020", "Rottweiler", "Zeus", "M", 36, "G", [], "2026-05-01", "Alta")
    score = adotante.calcular_pontuacao_compatibilidade(cachorro_g)
    assert score < 50

def test_compatibilidade_criancas_com_animal_arisco():
    """Adotante com crianças e animal arisco deve ter pontuação penalizada."""
    adotante = Adotante(
        "222.222.222-22", "Maria", 30, "88222222222", "maria@email.com",
        "casa", 100.0, True, {"tem_criancas": True}, {}, {"quantidade": 1}
    )
    gato_arisco = Gato("G010", "Persa", "Sombra", "F", 24, "P", ["Arisco"], "2026-06-01", "Alta")
    score_com_criancas = adotante.calcular_pontuacao_compatibilidade(gato_arisco)

    adotante_sem = Adotante(
        "333.444.555-66", "Sem Crianças", 30, "88000000001", "sc@email.com",
        "casa", 100.0, True, {}, {}, {"quantidade": 1}
    )
    score_sem_criancas = adotante_sem.calcular_pontuacao_compatibilidade(gato_arisco)
    assert score_com_criancas < score_sem_criancas


# ──────────────────────────────────────────────
# Repositório
# ──────────────────────────────────────────────

def test_repositorio_inserir_e_buscar(tmp_path):
    """Testa inserção e busca de um registro no repositório JSON."""
    from classes.infra import Repositorio
    repo = Repositorio(str(tmp_path / "dados.json"))

    repo.inserir("animais", {"id_animal": "C001", "nome": "Rex"})
    resultado = repo.buscar("animais", "id_animal", "C001")

    assert resultado is not None
    assert resultado["nome"] == "Rex"

def test_repositorio_atualizar(tmp_path):
    """Testa a atualização de um registro existente."""
    from classes.infra import Repositorio
    repo = Repositorio(str(tmp_path / "dados.json"))
    repo.inserir("animais", {"id_animal": "C002", "nome": "Bolinha", "status": "DISPONIVEL"})

    atualizado = repo.atualizar("animais", "id_animal", "C002", {"status": "ADOTADO"})
    assert atualizado is True
    assert repo.buscar("animais", "id_animal", "C002")["status"] == "ADOTADO"

def test_repositorio_deletar(tmp_path):
    """Testa a remoção de um registro."""
    from classes.infra import Repositorio
    repo = Repositorio(str(tmp_path / "dados.json"))
    repo.inserir("adotantes", {"cpf": "123", "nome": "Teste"})

    assert repo.deletar("adotantes", "cpf", "123") is True
    assert repo.buscar("adotantes", "cpf", "123") is None

def test_repositorio_busca_inexistente(tmp_path):
    """Testa que buscar registro ausente retorna None."""
    from classes.infra import Repositorio
    repo = Repositorio(str(tmp_path / "dados.json"))
    assert repo.buscar("animais", "id_animal", "NAO_EXISTE") is None


# ──────────────────────────────────────────────
# Políticas
# ──────────────────────────────────────────────

def test_politica_reserva_elegibilidade(adotante_basico, adotante_menor):
    """Testa validação de idade mínima na PoliticaReserva."""
    from classes.politicas import PoliticaReserva
    politica = PoliticaReserva()

    assert politica.validar_elegibilidade(adotante_basico) is True
    assert politica.validar_elegibilidade(adotante_menor) is False

def test_politica_adocao_moradia_porte_g():
    """Porte G em apartamento deve falhar na validação de moradia."""
    from classes.politicas import PoliticaAdocao
    politica = PoliticaAdocao()

    adotante_apto = Adotante(
        "333.333.333-33", "Carlos", 25, "88333333333", "c@c.com",
        "apto", 60.0, True, {}, {}, {}
    )
    cachorro_g = Cachorro("C030", "Pastor Alemão", "Brutus", "M", 48, "G", [], "2026-03-01", "Alta")
    assert politica.validar_moradia_porte(adotante_apto, cachorro_g) is False


# ──────────────────────────────────────────────
# Estratégias de taxa
# ──────────────────────────────────────────────

def test_senior_fee(cachorro_basico):
    """SeniorFee deve aplicar 50% de desconto sobre a taxa base."""
    from classes.taxas import SeniorFee
    assert SeniorFee().calcular_taxa(cachorro_basico) == 75.0

def test_puppy_fee(cachorro_basico):
    """PuppyFee deve incluir taxa base + vacinas + castração."""
    from classes.taxas import PuppyFee
    assert PuppyFee().calcular_taxa(cachorro_basico) == 350.0

def test_special_care_fee(cachorro_basico):
    """SpecialCareFee deve retornar taxa reduzida."""
    from classes.taxas import SpecialCareFee
    assert SpecialCareFee().calcular_taxa(cachorro_basico) == 50.0


# ──────────────────────────────────────────────
# Reserva
# ──────────────────────────────────────────────

def test_reserva_criacao_valida(cachorro_basico, adotante_basico):
    """Testa que uma reserva válida muda o status do animal para RESERVADO."""
    from classes.politicas import PoliticaReserva
    from classes.processos import Reserva

    reserva = Reserva("R001", cachorro_basico, adotante_basico, PoliticaReserva())
    assert reserva.status_reserva == "ativa"
    assert cachorro_basico.status == StatusAnimal.RESERVADO

def test_reserva_animal_indisponivel(adotante_basico):
    """Testa que reservar animal não disponível levanta ReservaInvalidaError."""
    from classes.politicas import PoliticaReserva
    from classes.processos import Reserva

    dog = Cachorro("C040", "Labrador", "Buddy", "M", 18, "M", [], "2026-07-01", "Alta")
    dog.mudar_status(StatusAnimal.INADOTAVEL)

    with pytest.raises(ReservaInvalidaError):
        Reserva("R002", dog, adotante_basico, PoliticaReserva())

def test_reserva_menor_de_idade(cachorro_basico, adotante_menor):
    """Adotante menor de idade não pode fazer reserva."""
    from classes.politicas import PoliticaReserva
    from classes.processos import Reserva

    with pytest.raises(PoliticaNaoAtendidaError):
        Reserva("R003", cachorro_basico, adotante_menor, PoliticaReserva())


# ──────────────────────────────────────────────
# Fila de espera
# ──────────────────────────────────────────────

def test_fila_espera_ordenacao(cachorro_basico):
    """Adotante com maior pontuação deve ser o próximo da fila."""
    from classes.infra import FilaEspera

    adotante_fraco = Adotante(
        "444.444.444-44", "Fraco", 19, "88444444444", "f@f.com",
        "apto", 30.0, False, {}, {}, {}
    )
    adotante_forte = Adotante(
        "555.555.555-55", "Forte", 28, "88555555555", "g@g.com",
        "casa", 200.0, True, {}, {}, {"quantidade": 3}
    )

    fila = FilaEspera(cachorro_basico)
    fila.adicionar(adotante_fraco, "2026-10-01T08:00:00")
    fila.adicionar(adotante_forte, "2026-10-01T09:00:00")

    assert len(fila) == 2
    assert fila.proximo().nome == "Forte"

def test_fila_espera_remover(cachorro_basico, adotante_basico):
    """Testa remoção de adotante da fila."""
    from classes.infra import FilaEspera

    fila = FilaEspera(cachorro_basico)
    fila.adicionar(adotante_basico)
    assert len(fila) == 1
    assert fila.remover(adotante_basico) is True
    assert len(fila) == 0
