# Guia do Produto: CoffeeMaster

## Visão Geral
O **CoffeeMaster** é um agente inteligente no Google Chat, focado na gestão eficiente e direta do estoque de café do escritório. Utilizando o Google ADK e Gemini 1.5 Flash, o agente foca em respostas ultracurtas visando economia de tokens.

## Público-Alvo e Uso
Destinado a **todos os funcionários** do setor e à **equipe da copa**. O agente permite:
- Registrar o consumo diário fixo: A copeira realiza o preparo diário (dias úteis) de duas garrafas (uma de 1L e outra de 2L). O sistema deve facilitar o abatimento contínuo desse volume no estoque.
- Registrar quando um funcionário realiza uma nova compra de suprimentos.
- Gerenciar um **rodízio de compras**, determinando e avisando de forma justa quem é o próximo funcionário responsável por comprar pó/filtros.

## Funcionalidades Essenciais (MVP)
1. **Gestão de Estoque:** Controle de entradas e saídas (abatimento do consumo diário de 3L de café) em gramas de pó e unidades de filtro.
2. **Alertas Proativos:** Notificações automáticas quando o estoque atinge o limite mínimo estipulado.
3. **Controle de Rodízio:** Determinação automática de quem deverá providenciar a próxima recarga de suprimentos, baseado no histórico.

## Visão de Futuro
O princípio norteador é a **Simplicidade Extrema**. O sistema não deve ser inchado com outras integrações ou gestão de novos produtos. Seu único e perfeito propósito é manter o café fluindo no escritório.