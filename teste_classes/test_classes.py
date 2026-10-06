import pytest
from classes.status_animal import StatusAnimal
from classes.cachorro import Cachorro
from classes.gato import Gato
from classes.adotante import Adotante


def test_criacao_cachorro():
    """Testa a criação de um cachorro e herança de atributos."""
    dog = Cachorro(
        id_animal="C001", raca="Vira-lata", nome="Rex", sexo="M",
        idade_meses=24, porte="M", temperamento=["Brincalhão"],
        data_entrada="2026-10-01", necessidade_passeio="Alta"
    )
    
    assert dog.nome == "Rex"
    assert dog.especie == "cachorro"
    assert dog.porte == "M"
    assert dog.status == StatusAnimal.DISPONIVEL

def test_encapsulamento_porte_animal_invalido():
    """Testa se o @property impede porte inválido."""
    with pytest.raises(ValueError, match="O porte deve ser obrigatoriamente 'P', 'M' ou 'G'."):
        Gato(
            id_animal="G001", raca="Siamês", nome="Mia", sexo="F",
            idade_meses=12, porte="X", temperamento=["Calma"], # 'X' é inválido
            data_entrada="2026-10-02", independencia="Alta"
        )

def test_encapsulamento_idade_negativa():
    """Testa se o @property impede idades negativas."""
    with pytest.raises(ValueError, match="A idade do animal não pode ser negativa."):
        Cachorro(
            id_animal="C002", raca="Poodle", nome="Bidu", sexo="M",
            idade_meses=-5, porte="P", temperamento=[], # '-5' é inválido
            data_entrada="2026-10-05", necessidade_passeio="Média"
        )

def test_metodos_especiais_animal():
    """Testa os métodos __eq__, __str__ e __iter__."""
    dog1 = Cachorro("1", "Pug", "Puggy", "M", 10, "P", [], "2026-10-01", "Baixa")
    dog2 = Cachorro("1", "Pug", "Puggy", "M", 10, "P", [], "2026-10-01", "Baixa")
    
    # Testa igualdade (__eq__) baseada no ID
    assert dog1 == dog2
    
    # Testa a representação em string (__str__)
    assert "Puggy (cachorro - Pug)" in str(dog1)
    
    # Testa o iterador de histórico (__iter__) e adição de evento
    dog1.registrar_evento("Chegou ao abrigo")
    dog1.vacinar("Raiva")
    
    historico = list(dog1) # Dispara o __iter__
    assert len(historico) == 1
    assert historico[0] == "Chegou ao abrigo"

def test_criacao_adotante_e_moradia():
    """Testa a criação do adotante e a validação da propriedade moradia."""
    adotante = Adotante(
        cpf="123.456.789-00", nome="Diêgo", idade=20, telefone="88999999999",
        email="diego@email.com", moradia="casa", area_util=150.0,
        experiencia_pets=True, criancas={}, outros_animais={}, experiencia_anterior={}
    )
    assert adotante.nome == "Diêgo"
    assert adotante.moradia == "casa"

    # Testa alteração para valor inválido
    with pytest.raises(ValueError):
        adotante.moradia = "fazenda"