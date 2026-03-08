from google.adk.agents.llm_agent import Agent
from inventory import register_daily_prep, get_next_buyer, register_purchase, get_inventory, update_stock
import os
from dotenv import load_dotenv

load_dotenv()

def registrar_preparo_diario():
    """Registra o preparo das 2 garrafas diárias (3L totais) e abate o estoque fixo."""
    return register_daily_prep()

def ver_proximo_comprador():
    """Consulta quem é o funcionário responsável pela próxima compra de café."""
    return get_next_buyer()

def registrar_compra_suprimentos(funcionario: str, gramas_po: int, qtd_filtros: int):
    """Registra uma nova compra de suprimentos, atualiza o estoque e rotaciona o comprador da vez."""
    return register_purchase(funcionario, gramas_po, qtd_filtros)

def ver_status_estoque():
    """Consulta as quantidades atuais de pó de café, filtros e o comprador da vez."""
    return get_inventory()

def ajuste_manual_estoque(gramas_po: int = 0, qtd_filtros: int = 0):
    """Realiza ajustes manuais no estoque (ex: derramamentos ou uso extra). Use valores negativos para remover."""
    return update_stock(powder=gramas_po, filters=qtd_filtros)

coffee_agent = Agent(
    model='gemini-1.5-flash',
    name='CoffeeMaster',
    description="Administrador de estoque de café e rodízio de compras para o escritório.",
    instruction="""
    Você é o CoffeeMaster. Persona: ultra-objetiva, formal e focada em economia de tokens.
    Sua missão é gerenciar o estoque (pó de café e filtros) e o rodízio de compras entre os funcionários.
    
    DIRETRIZES DE RESPOSTA:
    - Seja extremamente direto. Use Texto Puro.
    - Se houver um ALERTA no retorno das ferramentas, inclua-o na resposta.
    - Quando alguém disser que a copeira fez o café, use 'registrar_preparo_diario'.
    - Quando alguém perguntar de quem é a vez, use 'ver_proximo_comprador'.
    - Quando alguém disser que comprou café, use 'registrar_compra_suprimentos'.
    - Para dúvidas gerais sobre quanto temos, use 'ver_status_estoque'.
    """,
    tools=[
        registrar_preparo_diario, 
        ver_proximo_comprador, 
        registrar_compra_suprimentos, 
        ver_status_estoque, 
        ajuste_manual_estoque
    ],
)
