# Stack Tecnológica: CoffeeMaster

## Núcleo de Inteligência
- **IA Framework:** Google Agent Developer Kit (ADK) - Utilizado para a orquestração do agente e integração de ferramentas.
- **Modelo:** Gemini 1.5 Flash - Escolhido pela alta velocidade e excelente custo-benefício (economia de tokens).

## Desenvolvimento e Execução
- **Linguagem:** Python 3.12+
- **Gerenciador de Pacotes:** uv (Astral) - Build otimizado com Docker BuildKit.
- **API Server:** FastAPI + Uvicorn - Provê o endpoint de webhook para o Google Chat.
- **Ambiente:** Docker & Docker Compose - Garante portabilidade e isolamento do serviço.

## Persistência e Integrações
- **Banco de Dados:** Arquivo JSON (`inventory.json`) - Armazenamento simplificado para controle de estoque e histórico de rodízio.
- **Interface Externa:** Google Chat API - Canal oficial de interação com os usuários.
- **Segurança:** Variáveis de ambiente via arquivos `.env`.