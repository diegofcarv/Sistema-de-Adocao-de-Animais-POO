# Estrutura do Sistema de Adoção (UML)

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

---

## Estados (Enum / State)

### STATUSANIMAL
**Valores:**
* DISPONIVEL
* RESERVADO
* ADOTADO
* DEVOLVIDO
* QUARENTENA
* INADOTAVEL

---

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
* **Atributos:** `especie`, `raça`, `nome`, `sexo`, `idade_meses`, `porte`, `temperamento`, `status` (Tipo: StatusAnimal), `historico_eventos`
* **Métodos Especiais:** `__str__()`, `__repr__()`, `__eq__()`, `__hash__()`, `__lt__()`, `__iter__()`

**Cachorro**
* **Herda de:** `Animal`
* **Atributos:** `necessidade_passeio`, `especie = "cachorro"`

**Gato**
* **Herda de:** `Animal`
* **Atributos:** `independencia`, `especie = "gato"`

### Pessoas e Adotantes

**Pessoa**
* **Atributos:** `nome`, `idade`

**Adotante**
* **Herda de:** `Pessoa`
* **Atributos:** `moradia` (casa/apto), `area_util`, `experiencia_pets` (sim/não), `criancas` (sim/não, idade, quantidade), `outros_animais` (sim/não, porte, quantidade), `experiencia_anterior` (sim/não, quantidade)

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

**Estratégias Concretas (Herdam de Politica):**
* PoliticaReserva
* PoliticaAdocao
* PoliticaDevolucao
* PoliticaQuarentena

### Processos e Infraestrutura

**Repositorio**
* **Atributos:** `caminho_arquivo`
* **Métodos:** `salvar()`, `carregar()`, `buscar()`, `deletar()`

**FilaEspera**
* **Atributos:** `animal`, `fila`
* **Métodos:** `adicionar()`, `remover()`, `proximo()`, `__len__()`, `comparadores_prioridade()` (ex: `__lt__` para ordenação da fila)

**Reserva**
* **Atributos:** `animal`, `adotante`, `politica_reserva`, `data_criacao`, `status_reserva`
* **Métodos:** `verificar_expiracao()`

**Adoção**
* **Atributos:** `reserva`, `politica_adocao`, `taxa` (Calculada via Strategy), `contrato`, `data_adocao`

**Devolução**
* **Atributos:** `adocao`, `motivo`, `data_devolucao`, `status`

---

## Relacionamentos
* **Adotante <-> Reserva:** Um adotante pode fazer uma ou mais reservas (conforme política).
* **Reserva <-> Animal:** Uma reserva bloqueia temporariamente um animal.
* **Reserva -> Adoção:** Uma adoção efetiva os dados de uma reserva prévia.
* **Adoção -> Devolução:** Uma devolução reverte o processo de uma adoção.
* **Animal <-> FilaEspera:** Um animal muito disputado possui uma fila de espera de vários adotantes.
* **Adotante -> Animal:** A compatibilidade é calculada entre os atributos de ambos.