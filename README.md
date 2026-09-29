# Sistema de Adoção de Animais

## Descrição

O Sistema de Adoção de Animais é um miniprojeto individual, referente a disciplina de Programação Orientada a Objetos e que visa auxiliar no gerenciamento do processo de adoção de animais.

O sistema permitirá cadastrar animais e adotantes, realizar a análise de compatibilidade entre eles, controlar reservas e adoções, registrar devoluções e manter uma fila de espera para animais mais disputados.

Também serão utilizadas políticas configuráveis para definir algumas regras do sistema, como idade mínima do adotante, regras relacionadas à moradia e ao porte do animal, duração das reservas e critérios de compatibilidade.

## Objetivo

O projeto tem como objetivo desenvolver um sistema utilizando conceitos de Programação Orientada a Objetos, aplicando herança, encapsulamento, relacionamentos entre classes e outros recursos estudados na disciplina.

A proposta é representar as principais entidades envolvidas no processo de adoção e organizar suas responsabilidades em diferentes classes.

## Estrutura planejada

### Animal

A classe `Animal` é uma classe abstrata que representa os animais do sistema.

Possui informações como:

- espécie
- raça
- nome
- sexo
- idade
- porte
- temperamento
- status
- histórico de eventos

As classes `Cachorro` e `Gato` herdam de `Animal`. Dessa forma, compartilham os atributos e comportamentos definidos na classe base, além de possuírem características específicas.

- `Cachorro`: possui uma característica relacionada à necessidade de passeio.
- `Gato`: possui uma característica relacionada à sua independência.

### Mixins

Serão utilizados dois mixins para representar comportamentos que podem ser compartilhados pelos animais:

- `VacinavelMixin`: controle de vacinação e agenda de vacinas.
- `AdestravelMixin`: controle do nível de adestramento e treinamento.

A classe `Animal` herdará os comportamentos desses dois mixins.

### Pessoa e Adotante

A classe `Pessoa` representará informações básicas de uma pessoa.

A classe `Adotante` herdará de `Pessoa` e possuirá informações relacionadas à adoção, como:

- moradia
- área útil
- experiência com animais
- presença de crianças
- presença de outros animais
- experiência anterior com pets

### Estratégias de taxa

Será utilizado o padrão Strategy para representar diferentes formas de cálculo de taxas.

A classe `BaseFeeStrategy` será a classe abstrata base, com o método `calcular_taxa()`.

As estratégias:

- `SeniorFee`
- `PuppyFee`
- `SpecialCareFee`

herdarão de `BaseFeeStrategy`.

### Política

A classe `Política` será utilizada como classe base para as regras do sistema.

As seguintes classes herdarão de `Política`:

- `PolíticaReserva`
- `PolíticaAdocao`
- `PolíticaDevolucao`
- `PolíticaQuarentena`

As configurações das políticas serão definidas pelo arquivo `settings.json`.

Entre as configurações previstas estão:

- idade mínima do adotante
- regras de moradia e porte
- duração da reserva
- pesos de compatibilidade
- estratégia padrão de taxa

### Reserva

Representa a reserva de um animal por um adotante.

A reserva terá informações sobre:

- animal
- adotante
- política de reserva
- data de criação
- status da reserva

Também será responsável por verificar sua expiração.

### Adoção

Representa a realização da adoção de um animal.

Possui informações relacionadas à reserva, política de adoção, taxa, contrato e data da adoção.

### Devolução

Representa a devolução de um animal após uma adoção.

Possui informações sobre:

- adoção
- motivo
- data da devolução
- status

### FilaEspera

Representa a fila de espera para animais que possuem mais de um interessado.

Será responsável por adicionar, remover e consultar os adotantes da fila.

### Repositorio

Será responsável pela persistência dos dados do sistema.

Entre suas operações estão:

- salvar
- carregar
- buscar
- deletar

## Status dos animais

Os animais poderão possuir os seguintes estados:

- `DISPONIVEL`
- `RESERVADO`
- `ADOTADO`
- `DEVOLVIDO`
- `QUARENTENA`
- `INADOTAVEL`

## Relacionamentos principais

- Um `Adotante` pode realizar reservas.
- Uma `Reserva` está relacionada a um `Animal`.
- Uma `Reserva` pode resultar em uma `Adocao`.
- Uma `Adocao` pode estar relacionada a uma `Devolucao`.
- Um `Animal` pode possuir uma `FilaEspera`.
- A compatibilidade é calculada considerando informações do `Adotante` e do `Animal`.

## Configurações

O arquivo `settings.json` será utilizado para armazenar configurações que podem ser alteradas sem modificar diretamente as classes do sistema.

As principais configurações previstas são:

```json
{
    "idade_minima_adotante": 18,
    "regras_moradia_porte": {},
    "duracao_reserva": 48,
    "pesos_compatibilidade": {},
    "estrategia_taxa_padrao": ""
}