from google.adk.agents.llm_agent import Agent
from .inventory import register_daily_prep, get_next_buyer, register_purchase, get_inventory, update_stock
import os
from dotenv import load_dotenv

load_dotenv()

def registrar_preparo_diario():
    """Registra o consumo padrão diário (180g de pó e 2 filtros). Use sempre que um novo ciclo de café for iniciado."""
    return register_daily_prep()

def ver_proximo_comprador():
    """Consulta o nome do funcionário responsável pela próxima compra no sistema de rodízio."""
    return get_next_buyer()

def registrar_compra_suprimentos(funcionario: str, gramas_po: int, qtd_filtros: int):
    """
    Registra a entrada de novos insumos no estoque. 
    Args:
        funcionario: Nome de quem comprou.
        gramas_po: Quantidade exata em gramas (ex: 500).
        qtd_filtros: Número de unidades de filtros (ex: 30).
    """
    return register_purchase(funcionario, gramas_po, qtd_filtros)

def ver_status_estoque():
    """Consulta o inventário atual: gramas de pó, filtros e comprador da vez."""
    return get_inventory()

def ajuste_manual_estoque(gramas_po: int = 0, qtd_filtros: int = 0):
    """
    Ajusta o estoque para casos excepcionais (derramamentos ou doações).
    Args:
        gramas_po: Gramas a adicionar (positivo) ou remover (negativo).
        qtd_filtros: Unidades a adicionar (positivo) ou remover (negativo).
    """
    return update_stock(powder=gramas_po, filters=qtd_filtros)

root_agent = Agent(
    model='gemini-3.1-flash-lite-preview',
    name='CoffeeMaster',
    description="Administrador de elite para controle de insumos de café e rodízio de equipe.",
    instruction="""
    Você é o CoffeeMaster, um sistema operacional de gestão de café.
    REGRAS DE OURO:
    1. Responda APENAS com os dados brutos.
    2. PROIBIDO: saudações ("Olá", "Bom dia"), preâmbulos ou cortesias.
    3. FORMATO: [CHAVE]: [VALOR].
    4. ALERTAS: Se a ferramenta retornar 'ALERTA', exiba-o no topo da resposta em caixa alta.
    5. UNIDADES: Sempre use 'g' para pó e 'un' para filtros.
    
    EXEMPLO DE RESPOSTA:
    ALERTA: CAFÉ BAIXO!
    Pó: 150g
    Filtros: 12un
    Próximo: Gustavo
    """,
    tools=[
        registrar_preparo_diario, 
        ver_proximo_comprador, 
        registrar_compra_suprimentos, 
        ver_status_estoque, 
        ajuste_manual_estoque
    ],
)
