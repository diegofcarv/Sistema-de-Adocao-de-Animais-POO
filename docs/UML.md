# Estrutura do Sistema de Adoção de Animais (Textual)

## Entidades
* Animal
* Pessoa
* Adotante
* Reserva
* Adoção
* Devolução
* Fila de Espera
* Repositório
* Política

## Estados (Enum / State)

### STATUSANIMAL
**Valores:**
* DISPONIVEL
* RESERVADO
* ADOTADO
* DEVOLVIDO
* QUARENTENA
* INADOTAVEL

## Classes

### Mixins

**VacinavelMixin**
* **Atributos:** `historico_vacinas`, `proxima_vacina`
* **Métodos:** `vacinar()`, `agenda_vacinas()`

**AdestravelMixin**
* **Atributos:** `nivel_adestramento`
* **Métodos:** `treinar()`

### Animais

**Animal (Abstrata)**
* **Herda de:** `VacinavelMixin`, `AdestravelMixin`
* **Atributos:** `id_animal`, `especie`, `raça`, `nome`, `sexo`, `idade_meses`, `porte`, `temperamento`, `status` (Tipo: StatusAnimal), `historico_eventos`
* **Métodos:** `mudar_status()`, `registrar_evento()`
* **Métodos Especiais:** `__str__()`, `__repr__()`, `__eq__()`, `__hash__()`, `__lt__()`, `__iter__()`

**Cachorro**
* **Herda de:** `Animal`
* **Atributos:** `necessidade_passeio`, `especie = "cachorro"`

**Gato**
* **Herda de:** `Animal`
* **Atributos:** `independencia`, `especie = "gato"`

### Pessoas e Adotantes

**Pessoa**
* **Atributos:** `cpf`, `nome`, `idade`, `telefone`, `email`

**Adotante**
* **Herda de:** `Pessoa`
* **Atributos:** `moradia` (casa/apto), `area_util`, `experiencia_pets` (sim/não), `criancas` (sim/não, idade, quantidade), `outros_animais` (sim/não, porte, quantidade), `experiencia_anterior` (sim/não, quantidade)
* **Métodos:** `calcular_pontuacao_compatibilidade(animal)`

### Padrão Strategy (Taxas)

**BaseFeeStrategy (Interface/Abstrata)**
* **Métodos:** `calcular_taxa()`

**Estratégias Concretas (Herdam de BaseFeeStrategy):**
* SeniorFee
* PuppyFee
* SpecialCareFee

### Políticas

**Politica (Superclasse)**
* **Atributos:** `settings.json` (arquivo lido para definir pesos e regras)
* **Métodos:** `carregar_configuracoes()`

**Estratégias Concretas (Herdam de Politica):**
* PoliticaReserva: `validar_elegibilidade()`, `obter_duracao_reserva()`
* PoliticaAdocao: `validar_idade_minima()`, `validar_moradia_porte()`
* PoliticaDevolucao
* PoliticaQuarentena

### Processos e Infraestrutura

**Repositorio**
* **Atributos:** `caminho_arquivo`
* **Métodos:** `salvar()`, `carregar()`, `buscar()`, `deletar()`, `inserir()`, `atualizar()`

**FilaEspera**
* **Atributos:** `animal`, `fila` (Lista de Adotantes com `data_entrada`)
* **Métodos:** `adicionar()`, `remover()`, `proximo()`, `notificar_proximo()`, `__len__()`, `comparadores_prioridade()` (ex: `__lt__` para ordenação da fila por pontuação e tempo)

**Reserva**
* **Atributos:** `id_reserva`, `animal`, `adotante`, `politica_reserva`, `data_criacao`, `status_reserva`
* **Métodos:** `verificar_expiracao()`, `cancelar()`, `confirmar()`

**Adoção**
* **Atributos:** `id_adocao`, `reserva`, `politica_adocao`, `taxa` (Calculada via Strategy), `contrato`, `data_adocao`
* **Métodos:** `efetivar()`, `gerar_contrato()`

**Devolução**
* **Atributos:** `id_devolucao`, `adocao`, `motivo`, `condicao_animal`, `data_devolucao`, `status`
* **Métodos:** `processar_devolucao()`, `reavaliar_animal()`

## Relacionamentos
* **Adotante <-> Reserva:** Um adotante pode fazer uma ou mais reservas (conforme política).
* **Reserva <-> Animal:** Uma reserva bloqueia temporariamente um animal.
* **Reserva -> Adoção:** Uma adoção efetiva os dados de uma reserva prévia.
* **Adoção -> Devolução:** Uma devolução reverte o processo de uma adoção.
* **Animal <-> FilaEspera:** Um animal muito disputado possui uma fila de espera de vários adotantes.
* **Adotante -> Animal:** A compatibilidade é calculada entre os atributos de ambos.

## Exceções Customizadas
* `ReservaInvalidaError` — disparada quando uma reserva viola as regras de política
* `TransicaoDeEstadoInvalidaError` — disparada quando uma transição de status não é permitida
* `PoliticaNaoAtendidaError` — disparada quando um adotante não atende aos critérios de elegibilidade
* `RepositorioError` — disparada quando ocorre falha ao salvar ou carregar dados