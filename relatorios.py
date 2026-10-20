"""
Módulo de relatórios do Sistema de Adoção de Animais.

Gera relatórios sobre animais disponíveis, adotados e estatísticas do sistema.
"""
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from classes.animal import Animal
    from classes.adotante import Adotante


def relatorio_animais_por_status(animais: List["Animal"]) -> str:
    """
    Gera um relatório simples listando animais agrupados por status.

    Args:
        animais (list[Animal]): Lista de todos os animais do sistema.

    Returns:
        str: Relatório formatado em texto.
    """
    from classes.status_animal import StatusAnimal

    grupos: Dict[str, List] = {s.value: [] for s in StatusAnimal}
    for animal in animais:
        grupos[animal.status.value].append(animal)

    linhas = ["====== RELATÓRIO DE ANIMAIS POR STATUS ======\n"]
    for status, lista in grupos.items():
        linhas.append(f"[{status}] — {len(lista)} animal(is)")
        for a in lista:
            linhas.append(f"  • {a.nome} ({getattr(a, 'especie', '?')} - {a.raca}, porte {a.porte})")
        linhas.append("")

    return "\n".join(linhas)


def relatorio_disponiveis(animais: List["Animal"]) -> str:
    """
    Lista apenas os animais disponíveis para adoção.

    Args:
        animais (list[Animal]): Lista de todos os animais do sistema.

    Returns:
        str: Relatório formatado em texto.
    """
    from classes.status_animal import StatusAnimal

    disponiveis = [a for a in animais if a.status == StatusAnimal.DISPONIVEL]
    linhas = [f"====== ANIMAIS DISPONÍVEIS PARA ADOÇÃO ({len(disponiveis)}) ======\n"]

    if not disponiveis:
        linhas.append("Nenhum animal disponível no momento.")
    else:
        for a in sorted(disponiveis):  # ordenado por data de entrada (__lt__)
            linhas.append(
                f"  [{a.id_animal}] {a.nome} — {getattr(a, 'especie', '?')}, "
                f"raça: {a.raca}, porte: {a.porte}, idade: {a.idade_meses} meses"
            )

    return "\n".join(linhas)


def relatorio_compatibilidade(adotante: "Adotante", animais: List["Animal"]) -> str:
    """
    Calcula e lista a pontuação de compatibilidade de um adotante com cada animal disponível.

    Args:
        adotante (Adotante): O adotante a ser avaliado.
        animais (list[Animal]): Lista de animais.

    Returns:
        str: Relatório ordenado do mais ao menos compatível.
    """
    from classes.status_animal import StatusAnimal

    disponiveis = [a for a in animais if a.status == StatusAnimal.DISPONIVEL]
    scores = [
        (a, adotante.calcular_pontuacao_compatibilidade(a))
        for a in disponiveis
    ]
    scores.sort(key=lambda x: x[1], reverse=True)

    linhas = [f"====== COMPATIBILIDADE: {adotante.nome} ======\n"]
    for animal, score in scores:
        linhas.append(
            f"  {score:5.1f} pts — {animal.nome} "
            f"({getattr(animal, 'especie', '?')} - {animal.raca}, porte {animal.porte})"
        )

    return "\n".join(linhas)
