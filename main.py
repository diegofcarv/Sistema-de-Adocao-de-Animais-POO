import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

from classes.sistema_adocao import SistemaAdocao
from classes.excecoes import ReservaInvalidaError, PoliticaNaoAtendidaError, RepositorioError

# ── Funções Auxiliares de Validação de Input ──

def obter_inteiro(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Erro: Por favor, digite apenas números inteiros.")

def obter_float(prompt: str) -> float:
    while True:
        try:
            valor = input(prompt).replace(',', '.')
            return float(valor)
        except ValueError:
            print("Erro: Digite um número válido (ex: 120.5).")

def obter_sim_nao(prompt: str) -> bool:
    while True:
        resposta = input(prompt).strip().lower()
        if resposta in ['s', 'sim', 'y', 'yes']:
            return True
        elif resposta in ['n', 'nao', 'não', 'no']:
            return False
        print("Erro: Digite 'S' para Sim ou 'N' para Não.")

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# ── Telas de Interação ──

def tela_cadastrar_animal(sistema: SistemaAdocao):
    print("\n--- CADASTRO DE ANIMAL ---")
    while True:
        especie = input("Espécie (cachorro/gato): ").strip().lower()
        if especie in ['cachorro', 'gato']:
            break
        print("Espécie inválida.")

    dados = {
        'especie': especie,
        'id_animal': input("ID do animal (ex: C001): ").strip().upper(),
        'raca': input("Raça: ").strip().title(),
        'nome': input("Nome do animal: ").strip().title(),
        'sexo': input("Sexo (M/F): ").strip().upper(),
        'idade_meses': obter_inteiro("Idade (em meses): "),
        'porte': input("Porte (P/M/G): ").strip().upper(),
        'temperamento': input("Temperamento (separado por vírgula): ").split(','),
        'data_entrada': input("Data de entrada (AAAA-MM-DD) ou deixe vazio para hoje: ").strip()
    }
    
    # Limpeza de temperamentos vazios
    dados['temperamento'] = [t.strip() for t in dados['temperamento'] if t.strip()]

    if especie == 'cachorro':
        dados['necessidade_passeio'] = input("Necessidade de passeio (baixa/media/alta): ").strip().lower() or 'media'
    else:
        dados['independencia'] = input("Nível de independência (baixa/media/alta): ").strip().lower() or 'media'

    mensagem = sistema.cadastrar_animal(dados)
    print(f"\n {mensagem}")


def tela_listar_animais(sistema: SistemaAdocao):
    print("\n--- LISTA DE ANIMAIS ---")
    status = input("Filtrar por status (Deixe em branco para todos, ou digite DISPONIVEL, RESERVADO, etc): ").strip().upper()
    animais = sistema.listar_animais(status=status if status else None)
    
    if not animais:
        print("Nenhum animal encontrado.")
        return
        
    print(f"\n{'ID':<8} {'Nome':<15} {'Espécie':<10} {'Raça':<15} {'Porte':<6} {'Status'}")
    print('-' * 70)
    for a in animais:
        print(f"{a['id_animal']:<8} {a['nome']:<15} {a['especie']:<10} {a['raca']:<15} {a['porte']:<6} {a['status']}")


def tela_cadastrar_adotante(sistema: SistemaAdocao):
    print("\n--- CADASTRO DE ADOTANTE ---")
    dados = {
        'cpf': input("CPF (apenas números ou com formatação): ").strip(),
        'nome': input("Nome Completo: ").strip().title(),
        'idade': obter_inteiro("Idade: "),
        'telefone': input("Telefone: ").strip(),
        'email': input("E-mail: ").strip(),
        'moradia': input("Moradia (casa/apto): ").strip().lower(),
        'area_util': obter_float("Área útil da residência (m²): "),
        'experiencia_pets': obter_sim_nao("Já possuiu pets antes? (s/n): "),
        'criancas': {'tem_criancas': obter_sim_nao("Tem crianças em casa? (s/n): ")},
        'outros_animais': {'tem_outros': obter_sim_nao("Tem outros animais atualmente? (s/n): ")},
        'experiencia_anterior': {'quantidade': obter_inteiro("Quantos pets já teve? ")}
    }
    
    mensagem = sistema.cadastrar_adotante(dados)
    print(f"\n {mensagem}")


def tela_listar_adotantes(sistema: SistemaAdocao):
    print("\n--- LISTA DE ADOTANTES ---")
    adotantes = sistema.listar_adotantes()
    if not adotantes:
        print("Nenhum adotante cadastrado.")
        return
    print(f"\n{'CPF':<15} {'Nome':<20} {'Idade':<6} {'Moradia'}")
    print('-' * 55)
    for a in adotantes:
        print(f"{a['cpf']:<15} {a['nome']:<20} {a['idade']:<6} {a['moradia']}")


def tela_reservar(sistema: SistemaAdocao):
    print("\n--- RESERVAR ANIMAL ---")
    animal_id = input("ID do animal desejado: ").strip().upper()
    adotante_cpf = input("CPF do adotante: ").strip()
    
    mensagem = sistema.reservar(animal_id, adotante_cpf)
    print(f"\n {mensagem}")


def tela_adotar(sistema: SistemaAdocao):
    print("\n--- EFETIVAR ADOÇÃO ---")
    animal_id = input("ID do animal reservado: ").strip().upper()
    adotante_cpf = input("CPF do adotante: ").strip()
    
    contrato = sistema.adotar(animal_id, adotante_cpf)
    print("\n" + "="*40)
    print("CONTRATO GERADO COM SUCESSO:")
    print("="*40)
    print(contrato)


def tela_devolver(sistema: SistemaAdocao):
    print("\n--- DEVOLVER ANIMAL ---")
    animal_id = input("ID do animal a ser devolvido: ").strip().upper()
    motivo = input("Motivo da devolução (ex: incompatibilidade_comportamental): ").strip().lower()
    condicao = input("Condição física do animal (ex: saudavel, doente): ").strip().lower()
    
    mensagem = sistema.devolver(animal_id, motivo, condicao)
    print(f"\n {mensagem}")


def tela_compatibilidade(sistema: SistemaAdocao):
    print("\n--- VERIFICAR COMPATIBILIDADE ---")
    adotante_cpf = input("CPF do adotante: ").strip()
    
    resultado = sistema.compatibilidade(adotante_cpf)
    if not resultado:
        print("Nenhum animal disponível para comparar ou adotante não encontrado.")
        return
        
    print(f"\n{'Pontuação':<10} {'ID':<8} {'Nome':<15} {'Espécie':<10} {'Porte'}")
    print('-' * 60)
    for animal, score in resultado:
        print(f"{score:<10.1f} {animal['id_animal']:<8} {animal['nome']:<15} {animal['especie']:<10} {animal['porte']}")


def tela_seed(sistema: SistemaAdocao):
    print("\n--- GERANDO DADOS DE EXEMPLO ---")
    animais = [
        {'especie': 'cachorro', 'id_animal': 'C001', 'raca': 'Labrador', 'nome': 'Thor',
         'sexo': 'M', 'idade_meses': 6, 'porte': 'G', 'temperamento': ['Brincalhao', 'Docil'],
         'necessidade_passeio': 'alta'},
        {'especie': 'gato', 'id_animal': 'G001', 'raca': 'Siames', 'nome': 'Luna',
         'sexo': 'F', 'idade_meses': 24, 'porte': 'P', 'temperamento': ['Independente'],
         'independencia': 'alta'}
    ]
    adotantes = [
        {'cpf': '111.111.111-11', 'nome': 'Ana Lima', 'idade': 28, 'telefone': '88911111111',
         'email': 'ana@email.com', 'moradia': 'casa', 'area_util': 120.0,
         'experiencia_pets': True, 'criancas': {'tem_criancas': False},
         'outros_animais': {'tem_outros': False}, 'experiencia_anterior': {'quantidade': 2}}
    ]

    for a in animais:
        try:
            sistema.cadastrar_animal(a)
            print(f"Cadastrado animal: {a['nome']}")
        except ValueError:
            pass

    for a in adotantes:
        try:
            sistema.cadastrar_adotante(a)
            print(f"Cadastrado adotante: {a['nome']}")
        except ValueError:
            pass
    print(" Seed finalizado!")

# ── Loop Principal ──

def main():
    sistema = SistemaAdocao()
    
    while True:
        print("\n" + "="*40)
        print("SISTEMA DE ADOÇÃO DE ANIMAIS")
        print("="*40)
        print("1. Cadastrar novo animal")
        print("2. Listar animais")
        print("3. Cadastrar novo adotante")
        print("4. Listar adotantes")
        print("5. Reservar animal")
        print("6. Efetivar adoção (Gerar Contrato)")
        print("7. Devolver animal")
        print("8. Verificar compatibilidade (Match)")
        print("-" * 40)
        print("99. Inserir dados de exemplo (Seed)")
        print("0. Sair do sistema")
        print("="*40)
        
        opcao = input("Escolha uma opção: ").strip()
        limpar_tela()

        try:
            if opcao == '1': tela_cadastrar_animal(sistema)
            elif opcao == '2': tela_listar_animais(sistema)
            elif opcao == '3': tela_cadastrar_adotante(sistema)
            elif opcao == '4': tela_listar_adotantes(sistema)
            elif opcao == '5': tela_reservar(sistema)
            elif opcao == '6': tela_adotar(sistema)
            elif opcao == '7': tela_devolver(sistema)
            elif opcao == '8': tela_compatibilidade(sistema)
            elif opcao == '99': tela_seed(sistema)
            elif opcao == '0':
                print("Encerrando o sistema. Até logo! 👋")
                break
            else:
                print(" Opção inválida. Digite um número do menu.")
                
        except (ReservaInvalidaError, PoliticaNaoAtendidaError, RepositorioError) as e:
            print(f"\n ERRO DE NEGÓCIO: {e}")
        except ValueError as e:
            print(f"\n ERRO DE VALIDAÇÃO: {e}")
        except Exception as e:
            print(f"\n ERRO INESPERADO: {e}")
            
        input("\nPressione [ENTER] para voltar ao menu principal...")
        limpar_tela()

if __name__ == '__main__':
    main()