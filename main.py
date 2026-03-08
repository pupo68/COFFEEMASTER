from fastapi import FastAPI, Request
from agent import coffee_agent
from google.adk.runtime.runner import Runner
import uvicorn
import asyncio

app = FastAPI()
runner = Runner(agent=coffee_agent)

@app.post("/")
async def handle_request(request: Request):
    event = await request.json()
    
    # Google Chat Event format
    # type: MESSAGE, ADDED_TO_SPACE, etc.
    if event.get("type") == "ADDED_TO_SPACE":
        return {"text": "CoffeeMaster online. Comandos: status, adicionei 500g, usei 1 filtro."}
    
    message = event.get("message", {}).get("text", "")
    if not message:
        return {"text": "Aguardando comando."}
    
    # Run the ADK Agent
    response = await runner.run(input_text=message)
    
    # Return formatted for Google Chat
    return {"text": response.output}

if __name__ == "__main__":
    # Para rodar: python main.py
    uvicorn.run(app, host="0.0.0.0", port=8080)
