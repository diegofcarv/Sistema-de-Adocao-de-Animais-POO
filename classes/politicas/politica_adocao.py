from .politica import Politica

class PoliticaAdocao(Politica):
    """Define e valida as regras estritas para a efetivação de uma adoção."""

    def validar_idade_minima(self, adotante) -> bool:
        """
        Valida se o adotante atingiu a idade mínima legal exigida.

        Args:
            adotante (Adotante): O adotante a ser avaliado.

        Returns:
            bool: True se a idade for suficiente.
        """
        config = self.carregar_configuracoes()
        idade_minima = config.get("idade_minima_adotante", 18)
        return adotante.idade >= idade_minima

    def validar_moradia_porte(self, adotante, animal) -> bool:
        """
        Valida se o tipo e área da moradia são compatíveis com o porte do animal.

        Args:
            adotante (Adotante): O adotante a ser avaliado.
            animal (Animal): O animal a ser adotado.

        Returns:
            bool: True se compatível.
        """
        config = self.carregar_configuracoes()
        regras = config.get("regras_moradia_porte", {})
        porte = animal.porte

        if porte == "G":
            regra = regras.get("G", {})
            if adotante.moradia != "casa":
                return False
            if adotante.area_util < regra.get("area_minima", 80):
                return False
        elif porte == "M":
            regra = regras.get("M", {})
            if adotante.moradia == "apto":
                if adotante.area_util < regra.get("area_minima_apto", 50):
                    return False
        return True
