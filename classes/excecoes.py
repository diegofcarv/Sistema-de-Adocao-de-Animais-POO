class ReservaInvalidaError(Exception):
    """Disparada quando uma reserva viola as regras de política."""
    pass

class TransicaoDeEstadoInvalidaError(Exception):
    """Disparada quando uma transição de status não é permitida."""
    pass

class PoliticaNaoAtendidaError(Exception):
    """Disparada quando um adotante não atende aos critérios de elegibilidade."""
    pass

class RepositorioError(Exception):
    """Disparada quando ocorre falha ao salvar ou carregar dados."""
    pass
