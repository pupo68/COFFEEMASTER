# Dossiê Estratégico: Modelos Gemini API (Março 2026)

Este documento consolida as especificações técnicas, capacidades e custos de todos os modelos disponíveis na Gemini API, com foco em otimização para agentes de IA e economia de tokens.

---

## 1. Tabela Comparativa de Preços (Tier Pago)
*Preços por 1 Milhão (1M) de tokens em USD (Dólar).*

| Família | Modelo | Entrada (Prompt) | Saída (Resposta) | Contexto | Observação |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **3.1 (Latest)** | **Gemini 3.1 Pro** | $2.00 | $12.00 | 2M+ | Elite em Raciocínio |
| | **Gemini 3.1 Flash** | $0.25 | $1.50 | 1M | Alta Velocidade |
| | **3.1 Flash-Lite** | **$0.10** | **$0.40** | 1M | **Rei do Custo/Benefício** |
| **2.5 (Stable)** | **Gemini 2.5 Pro** | $1.25 | $10.00 | 2M | Estável/Produção |
| | **Gemini 2.5 Flash** | $0.30 | $2.50 | 1M | Equilibrado |
| | **2.5 Flash-Lite** | $0.10 | $0.40 | 1M | Econômico Estável |
| **2.0 (Fast)** | **Gemini 2.0 Flash** | $0.10 | $0.40 | 1M | Otimizado para Agents |
| **1.5 (Legacy)** | **Gemini 1.5 Flash** | $0.075 | $0.30 | 1M | Legado Barato |
| | **1.5 Flash-8B** | **$0.0375**| **$0.15** | 1M | **Menor Preço Absoluto** |

---

## 2. Análise por Perfil de Uso

### A. Otimização para Agentes (Tools/Function Calling)
- **Melhor Escolha:** `gemini-2.0-flash` ou `gemini-3.1-flash`.
- **Por que:** Estes modelos foram treinados especificamente para entender chamadas de funções (ferramentas) com menor taxa de erro. São ideais para o CoffeeMaster manipular o `inventory.json`.

### B. Economia Extrema de Tokens
- **Melhor Escolha:** `gemini-1.5-flash-8b` ou `gemini-3.1-flash-lite`.
- **Por que:** O modelo 8B é o mais barato da história da API, mas o 3.1 Flash-Lite oferece uma inteligência muito superior pela diferença mínima de preço, sendo mais resiliente a instruções complexas.

### C. Raciocínio Complexo e Código
- **Melhor Escolha:** `gemini-3.1-pro`.
- **Por que:** Utilizado para arquitetura de software, depuração profunda e análise de arquivos massivos.

---

## 3. Tecnologias de Redução de Custo

### Context Caching
- Permite armazenar partes repetitivas do prompt (como as instruções do CoffeeMaster e a lista de funcionários) no cache da Google.
- **Economia:** Até **90%** de redução no custo dos tokens de entrada para prompts longos.

### Batch API
- Para tarefas que não precisam de resposta imediata (ex: gerar relatórios semanais de consumo).
- **Economia:** **50% de desconto** fixo sobre o preço do modelo escolhido.

---

## 4. Recomendações para o Projeto CoffeeMaster

1. **Fase de Desenvolvimento:** Usar `gemini-3.1-flash` (mais inteligente para acertar a lógica inicial).
2. **Produção (Dia a Dia):** Migrar para `gemini-3.1-flash-lite`. 
   - *Estimativa de custo:* Com 100 interações diárias curtas, o custo mensal seria inferior a **$0.05 USD**.

---
*Dossiê gerado em 08 de março de 2026.*
