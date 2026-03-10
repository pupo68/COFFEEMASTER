from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from coffeemaster_agent.agent import root_agent
from coffeemaster_agent.inventory import get_inventory
from google.adk.apps import App
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai.types import Content, Part
import uvicorn
import os
from pathlib import Path

app = FastAPI(title="CoffeeMaster Backend Elite")

# Habilitar CORS para comunicação com o Frontend desacoplado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique a URL do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração de Persistência (Padrão Senior)
DB_PATH = Path("coffeemaster_agent/.adk/session.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH.absolute()}"

# Configuração da Aplicação ADK
adk_app = App(
    name="CoffeeMaster",
    root_agent=root_agent
)

# O Runner orquestra a execução da aplicação com auto-gerenciamento de sessão
session_service = DatabaseSessionService(db_url=DATABASE_URL)
runner = Runner(
    app=adk_app, 
    session_service=session_service,
    auto_create_session=True
)

# Modelos de Dados
class ChatRequest(BaseModel):
    message: str
    session_id: str = "web_user"

class ChatResponse(BaseModel):
    reply: str

# Endpoints da API
@app.get("/api/inventory")
async def api_get_inventory():
    return get_inventory()

@app.post("/api/chat", response_model=ChatResponse)
async def api_chat(request: ChatRequest):
    user_id = "web_user"
    
    try:
        # O Runner agora gerencia a sessão automaticamente (Padrão Sênior ADK)
        run_result = runner.run(
            user_id=user_id,
            session_id=request.session_id,
            new_message=Content(
                role="user",
                parts=[Part(text=request.message)]
            )
        )
        
        # Acumular todo o texto gerado durante o ciclo de vida da execução (Padrão Senior)
        accumulated_text = []
        for event in run_result:
            # Verifica se o evento contém conteúdo textual do modelo
            if hasattr(event, 'content') and event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        accumulated_text.append(part.text)
            
            # Caso especial: se o ADK fornecer um atributo direto de texto no evento
            elif hasattr(event, 'output_text') and event.output_text:
                accumulated_text.append(event.output_text)
        
        reply_text = "".join(accumulated_text).strip()
        
        # Se houve processamento mas nenhum texto foi gerado (ex: apenas uso de ferramentas)
        if not reply_text:
            reply_text = "Comando processado. Estoque atualizado."
            
        return ChatResponse(reply=reply_text)
        
    except Exception as e:
        print(f"Erro CoffeeMaster: {e}")
        return ChatResponse(reply="ERRO: O terminal de IA encontrou um problema técnico.")

if __name__ == "__main__":
    # Porta 1000 conforme diretrizes, reload ativo para desenvolvimento
    uvicorn.run("main:app", host="0.0.0.0", port=1000, reload=True)
