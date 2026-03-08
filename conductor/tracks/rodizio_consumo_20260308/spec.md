# Track specification: Implementar consumo automatizado de 3L e sistema de rodízio de compras

## Objetivo
Implementar a funcionalidade de abatimento fixo de estoque para o preparo diário (2 garrafas: 1L e 2L) e gerenciar a lista de funcionários para o rodízio de compras de suprimentos.

## Requisitos de Negócio
1. **Consumo Diário:** O agente deve permitir registrar o preparo das duas garrafas diárias (3L totais) de uma só vez. 
    - Deve-se calcular o peso de pó de café consumido (Padrão Internacional SCA: 6g por 100ml -> 180g por dia).
    - Deve-se abater as unidades de filtro utilizadas (2 filtros por dia).
2. **Sistema de Rodízio:**
    - O agente deve manter uma lista de funcionários que participam do rateio/compra.
    - O agente deve informar quem é o próximo comprador quando o estoque estiver baixo ou sob demanda.
    - Ao registrar uma nova compra, o agente deve marcar o comprador atual como "pago" e passar para o próximo da lista.
3. **Respostas Curtas:** Manter a persona objetiva e formal (Texto Puro).

## Especificações Técnicas
- **Dados:** Adicionar os campos `staff_list`, `last_buyer_index` e `consumption_config` no `inventory.json`.
- **Ferramentas (Tools):**
    - `register_daily_prep()`: Abate o pó e o filtro das garrafas de 1L e 2L.
    - `get_next_buyer()`: Retorna o nome do próximo funcionário da lista.
    - `register_purchase(staff_name)`: Adiciona estoque e rotaciona o comprador.
- **Modelo:** Gemini 1.5 Flash.