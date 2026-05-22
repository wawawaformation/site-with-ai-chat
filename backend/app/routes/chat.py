"""Endpoint de chat — STUB à implémenter par l'étudiant.

Étape 1 : remplacer la réponse 'TODO' par un appel direct à Kimi-K2.6 via
          AzureAIChatCompletionsModel (langchain-azure-ai), sans outils,
          qui renvoie la réponse du modèle.
AzureAIChatCompletionsModel
Étape 2 : transformer ça en agent LangChain avec 3 outils branchés sur app/store.py :
          - list_recipes  → retourne la liste actuelle
          - create_recipe → crée une nouvelle recette
          - delete_recipe → supprime par id
          (voir langchain.agents.create_agent)

Étape 3 (stretch) : mémoire conversationnelle pour suivre une session de chat.
"""

import os
from dotenv import load_dotenv

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


### 1 - configuration du llm avec Azure AI ###
load_dotenv()  # charge les variables d'environnement depuis le fichier .env

llm = AzureAIChatCompletionsModel(
    endpoint=os.getenv("AZURE_AI_INFERENCE_ENDPOINT"),
    model=os.getenv("AZURE_AI_INFERENCE_MODEL"),
    credential=os.getenv("AZURE_AI_INFERENCE_API_KEY"),
)

### 2 - configuration de l'agent sans outils pour l'instant (étape 1) ###
system_prompt = "Tu es un assistant de cuisine virtuel. Tu aides les utilisateurs à gérer leurs recettes de cuisine. Mais tu peux aussi parler de tout au besoin . Sois amical et serviable."
agent = create_agent(llm, tools=[], system_prompt=system_prompt)
router = APIRouter(prefix="/chat", tags=["chat"])




class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    
    ### 3 - appel à l'agent pour générer une réponse (étape 1) ###
    result = agent.invoke({"messages" : [{"role": "user", "content": request.message}]
        
    })
   
    #print("result from agent:", result)  # debug print pour voir la structure de la réponse
    return ChatResponse(
        ### 4 - retourner la réponse du modèle (étape 1) ###
        
        reply=result["messages"][-1].content # attention à la structure de la réponse content et pas ["content"]
    )
