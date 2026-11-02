# main.py
import argparse
import sys

from classes.sistema_adocao import SistemaAdocao
from classes.excecoes import ReservaInvalidaError, PoliticaNaoAtendidaError, RepositorioError


def cmd_cadastrar_animal(args):
    sistema = SistemaAdocao()
    temperamento = args.temperamento.split(',') if args.temperamento else []
    dados = {
        'especie': args.especie,
        'id_animal': args.id,
        'raca': args.raca,
        'nome': args.nome,
        'sexo': args.sexo,
        'idade_meses': args.idade_meses,
        'porte': args.porte,
        'temperamento': temperamento,
        'data_entrada': args.data_entrada,
        'necessidade_passeio': getattr(args, 'necessidade_passeio', 'media'),
        'independencia': getattr(args, 'independencia', 'media'),
    }
    sistema.cadastrar_animal(dados)


def cmd_listar_animais(args):
    sistema = SistemaAdocao()
    animais = sistema.listar_animais(status=args.status)
    if not animais:
        print("Nenhum animal encontrado.")
        return
    print(f"\n{'ID':<8} {'Nome':<15} {'Especie':<10} {'Raca':<15} {'Porte':<6} {'Status'}")
    print('-' * 65)
    for a in animais:
        print(f"{a['id_animal']:<8} {a['nome']:<15} {a['especie']:<10} {a['raca']:<15} {a['porte']:<6} {a['status']}")


def cmd_cadastrar_adotante(args):
    sistema = SistemaAdocao()
    dados = {
        'cpf': args.cpf,
        'nome': args.nome,
        'idade': args.idade,
        'telefone': args.telefone,
        'email': args.email,
        'moradia': args.moradia,
        'area_util': args.area_util,
        'experiencia_pets': args.experiencia_pets,
        'criancas': {'tem_criancas': args.criancas},
        'outros_animais': {'tem_outros': args.outros_animais},
        'experiencia_anterior': {'quantidade': args.experiencia_anterior},
    }
    sistema.cadastrar_adotante(dados)


def cmd_listar_adotantes(args):
    sistema = SistemaAdocao()
    adotantes = sistema.listar_adotantes()
    if not adotantes:
        print("Nenhum adotante cadastrado.")
        return
    print(f"\n{'CPF':<15} {'Nome':<20} {'Idade':<6} {'Moradia'}")
    print('-' * 50)
    for a in adotantes:
        print(f"{a['cpf']:<15} {a['nome']:<20} {a['idade']:<6} {a['moradia']}")


def cmd_reservar(args):
    sistema = SistemaAdocao()
    sistema.reservar(args.animal, args.adotante)


def cmd_adotar(args):
    sistema = SistemaAdocao()
    sistema.adotar(args.animal, args.adotante)


def cmd_devolver(args):
    sistema = SistemaAdocao()
    sistema.devolver(args.animal, args.motivo, args.condicao)


def cmd_compatibilidade(args):
    sistema = SistemaAdocao()
    resultado = sistema.compatibilidade(args.adotante)
    if not resultado:
        print("Nenhum animal disponível para comparar.")
        return
    print(f"\n{'Pontuacao':<10} {'ID':<8} {'Nome':<15} {'Especie':<10} {'Porte'}")
    print('-' * 55)
    for animal, score in resultado:
        print(f"{score:<10.1f} {animal['id_animal']:<8} {animal['nome']:<15} {animal['especie']:<10} {animal['porte']}")


def cmd_seed(args):
    """Cadastra dados de exemplo para demonstração."""
    sistema = SistemaAdocao()

    animais = [
        {'especie': 'cachorro', 'id_animal': 'C001', 'raca': 'Labrador', 'nome': 'Thor',
         'sexo': 'M', 'idade_meses': 6, 'porte': 'G', 'temperamento': 'Brincalhao,Docil',
         'data_entrada': '2026-09-01', 'necessidade_passeio': 'alta'},
        {'especie': 'cachorro', 'id_animal': 'C002', 'raca': 'Poodle', 'nome': 'Mel',
         'sexo': 'F', 'idade_meses': 96, 'porte': 'P', 'temperamento': 'Calmo,Carinhoso',
         'data_entrada': '2026-09-10', 'necessidade_passeio': 'baixa'},
        {'especie': 'gato', 'id_animal': 'G001', 'raca': 'Siames', 'nome': 'Luna',
         'sexo': 'F', 'idade_meses': 24, 'porte': 'P', 'temperamento': 'Independente',
         'data_entrada': '2026-09-15', 'independencia': 'alta'},
        {'especie': 'gato', 'id_animal': 'G002', 'raca': 'Persa', 'nome': 'Simba',
         'sexo': 'M', 'idade_meses': 8, 'porte': 'P', 'temperamento': 'Docil,Brincalhao',
         'data_entrada': '2026-10-01', 'independencia': 'media'},
    ]

    adotantes = [
        {'cpf': '111.111.111-11', 'nome': 'Ana Lima', 'idade': 28, 'telefone': '88911111111',
         'email': 'ana@email.com', 'moradia': 'casa', 'area_util': 120.0,
         'experiencia_pets': True, 'criancas': {'tem_criancas': False},
         'outros_animais': {'tem_outros': False},
         'experiencia_anterior': {'quantidade': 2}},
        {'cpf': '222.222.222-22', 'nome': 'Carlos Melo', 'idade': 35, 'telefone': '88922222222',
         'email': 'carlos@email.com', 'moradia': 'apto', 'area_util': 45.0,
         'experiencia_pets': False, 'criancas': {'tem_criancas': True},
         'outros_animais': {'tem_outros': False},
         'experiencia_anterior': {'quantidade': 0}},
    ]

    print("Cadastrando dados de exemplo...")
    for a in animais:
        try:
            a['temperamento'] = a['temperamento'].split(',')
            sistema.cadastrar_animal(a)
        except ValueError as e:
            print(f"  Aviso: {e}")

    for a in adotantes:
        try:
            sistema.cadastrar_adotante(a)
        except ValueError as e:
            print(f"  Aviso: {e}")

    print("Dados de exemplo cadastrados.")


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='python main.py',
        description='Sistema de Adocao de Animais'
    )
    sub = parser.add_subparsers(dest='comando', required=True)

    # cadastrar-animal
    p = sub.add_parser('cadastrar-animal', help='Cadastra um novo animal')
    p.add_argument('--especie', required=True, choices=['cachorro', 'gato'])
    p.add_argument('--id', required=True, help='ID unico do animal (ex: C001)')
    p.add_argument('--raca', required=True)
    p.add_argument('--nome', required=True)
    p.add_argument('--sexo', required=True, choices=['M', 'F'])
    p.add_argument('--idade-meses', dest='idade_meses', required=True, type=int)
    p.add_argument('--porte', required=True, choices=['P', 'M', 'G'])
    p.add_argument('--temperamento', help='Temperamentos separados por virgula')
    p.add_argument('--data-entrada', dest='data_entrada',
                   default=None, help='Data no formato AAAA-MM-DD')
    p.add_argument('--necessidade-passeio', dest='necessidade_passeio', default='media')
    p.add_argument('--independencia', default='media')
    p.set_defaults(func=cmd_cadastrar_animal)

    # listar-animais
    p = sub.add_parser('listar-animais', help='Lista os animais cadastrados')
    p.add_argument('--status', default=None,
                   help='Filtra por status: DISPONIVEL, RESERVADO, ADOTADO...')
    p.set_defaults(func=cmd_listar_animais)

    # cadastrar-adotante
    p = sub.add_parser('cadastrar-adotante', help='Cadastra um novo adotante')
    p.add_argument('--cpf', required=True)
    p.add_argument('--nome', required=True)
    p.add_argument('--idade', required=True, type=int)
    p.add_argument('--telefone', required=True)
    p.add_argument('--email', required=True)
    p.add_argument('--moradia', required=True, choices=['casa', 'apto'])
    p.add_argument('--area-util', dest='area_util', required=True, type=float)
    p.add_argument('--experiencia-pets', dest='experiencia_pets',
                   action='store_true', default=False)
    p.add_argument('--criancas', action='store_true', default=False)
    p.add_argument('--outros-animais', dest='outros_animais',
                   action='store_true', default=False)
    p.add_argument('--experiencia-anterior', dest='experiencia_anterior',
                   type=int, default=0)
    p.set_defaults(func=cmd_cadastrar_adotante)

    # listar-adotantes
    p = sub.add_parser('listar-adotantes', help='Lista os adotantes cadastrados')
    p.set_defaults(func=cmd_listar_adotantes)

    # reservar
    p = sub.add_parser('reservar', help='Reserva um animal para um adotante')
    p.add_argument('--animal', required=True, help='ID do animal')
    p.add_argument('--adotante', required=True, help='CPF do adotante')
    p.set_defaults(func=cmd_reservar)

    # adotar
    p = sub.add_parser('adotar', help='Efetiva a adocao de um animal reservado')
    p.add_argument('--animal', required=True, help='ID do animal')
    p.add_argument('--adotante', required=True, help='CPF do adotante')
    p.set_defaults(func=cmd_adotar)

    # devolver
    p = sub.add_parser('devolver', help='Registra a devolucao de um animal adotado')
    p.add_argument('--animal', required=True, help='ID do animal')
    p.add_argument('--motivo', required=True,
                   help='Motivo da devolucao (ex: incompatibilidade_comportamental)')
    p.add_argument('--condicao', required=True,
                   help='Condicao do animal (ex: saudavel, doente, agressivo)')
    p.set_defaults(func=cmd_devolver)

    # compatibilidade
    p = sub.add_parser('compatibilidade', help='Mostra compatibilidade de um adotante com os animais disponiveis')
    p.add_argument('--adotante', required=True, help='CPF do adotante')
    p.set_defaults(func=cmd_compatibilidade)

    # seed
    p = sub.add_parser('seed', help='Cadastra dados de exemplo para demonstracao')
    p.set_defaults(func=cmd_seed)

    return parser


def main():
    parser = criar_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except (ReservaInvalidaError, PoliticaNaoAtendidaError) as e:
        print(f"Erro de regra: {e}")
        sys.exit(1)
    except (ValueError, RepositorioError) as e:
        print(f"Erro: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()