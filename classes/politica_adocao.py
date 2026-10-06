from politica import Politica

class PoliticaAdocao(Politica):
    """Define e valida as regras estritas para a efetivação de uma adoção."""
    def validar_idade_minima(self) -> bool:
        """Valida se o adotante atingiu a idade mínima legal exigida (ex: 18 anos)."""
        pass

    def validar_moradia_porte(self) -> bool:
        """Valida se o tipo e área da moradia são compatíveis com o porte do animal."""
        pass