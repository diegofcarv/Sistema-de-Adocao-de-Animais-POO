from .animal import Animal
from .cachorro import Cachorro
from .gato import Gato


def animal_de_dict(dados: dict):
    """Reconstrói um Cachorro ou Gato a partir de um dicionário."""
    especie = dados.get("especie")
    if especie == "cachorro":
        return Cachorro.de_dict(dados)
    elif especie == "gato":
        return Gato.de_dict(dados)
    raise ValueError(f"Espécie desconhecida: {especie}")