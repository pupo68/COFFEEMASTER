# Implementation Plan: Implementar consumo automatizado de 3L e sistema de rodízio de compras

## Fase 1: Expansão de Dados e Lógica de Inventário
Nesta fase, prepararemos o `inventory.json` e as funções básicas de manipulação de dados.

- [ ] **Task: Atualizar o esquema do `inventory.json`**
    - [ ] Adicionar campos para lista de funcionários.
    - [ ] Adicionar campos para configurações de consumo (g/ml, filtros por preparo).
- [ ] **Task: Implementar lógica de rodízio em `inventory.py`**
    - [ ] Criar função `get_next_buyer_logic()`.
    - [ ] Criar função `rotate_buyer_logic()`.
- [ ] **Task: Conductor - User Manual Verification 'Fase 1' (Protocol in workflow.md)**

## Fase 2: Implementação das Ferramentas (Tools) do ADK
Integração da lógica de negócio com o agente de IA.

- [ ] **Task: Implementar `register_daily_prep` em `inventory.py`**
    - [ ] Criar testes unitários para o cálculo de consumo.
    - [ ] Implementar a função de abatimento.
- [ ] **Task: Atualizar `agent.py` com as novas ferramentas**
    - [ ] Registrar `register_daily_prep`, `get_next_buyer` e `register_purchase`.
    - [ ] Atualizar instruções (system instruction) para incluir a lógica de rodízio.
- [ ] **Task: Conductor - User Manual Verification 'Fase 2' (Protocol in workflow.md)**

## Fase 3: Validação e Integração Final
Teste de ponta a ponta e preparação para o Google Chat.

- [ ] **Task: Testar fluxo completo via CLI (adk run)**
    - [ ] Simular comando "fiz o café de hoje".
    - [ ] Simular comando "quem compra o próximo?".
- [ ] **Task: Validar persistência do Docker Volume**
    - [ ] Garantir que o `inventory.json` mapeado contém os novos dados do rodízio.
- [ ] **Task: Conductor - User Manual Verification 'Fase 3' (Protocol in workflow.md)**
