


from fastapi import APIRouter
from pydantic import BaseModel


from langchain_core.runnables import RunnableConfig
from langchain.agents import create_agent




from app.agent.agent import  agent






### 3 - configuration de l'agent avec outils (étape 2)  et sauvegarde de session (etape 3)###


router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default" #Il faudra en envpoyé un vrai qui vient du front


class ChatResponse(BaseModel):
    reply: str


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    ### On ajoute la memoire
    config: RunnableConfig = {"configurable": {"thread_id": "1"}}
    
    
    
    ### 3 - appel à l'agent pour générer une réponse (étape 1) ###
    result = agent.invoke(
        {"messages" : [{"role": "user", "content": request.message}]},
        config = config
        )
   

    return ChatResponse(
        ### 4 - retourner la réponse du modèle (étape 1) ###
        
        reply=result["messages"][-1].content # attention à la structure de la réponse content et pas ["content"]
    )
