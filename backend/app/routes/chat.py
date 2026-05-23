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
from langchain.tools import tool


from app.store import list_recipes, create_recipe, delete_recipe, RecipeCreate


### 1 - configuration du llm avec Azure AI ###
load_dotenv() 

llm = AzureAIChatCompletionsModel(
    endpoint=os.getenv("AZURE_AI_INFERENCE_ENDPOINT"),
    model=os.getenv("AZURE_AI_INFERENCE_MODEL"),
    credential=os.getenv("AZURE_AI_INFERENCE_API_KEY"),
)



### 2 - définition des outils pour l'agent (étape 2) ###

@tool
def list_recipes_tool() -> str:
    """Retourne la liste des recettes actuelles."""
    recipes = list_recipes()
    if not recipes:
        return "Aucune recette trouvée."
    return "Des recettes ont été trouvées : " + ", ".join(f"{r.name}" for r in recipes)

@tool
def create_recipe_tool(name: str, ingredients: list[str]) -> str:
    """Crée une nouvelle recette."""
    recipe = create_recipe(data=RecipeCreate(name=name, ingredients=ingredients))
    return f"Recette '{recipe.name}' créée avec succès."


@tool
def delete_recipe_tool(recipe_id: int) -> str:
    """Supprime une recette par ID."""
    success = delete_recipe(recipe_id)
    if success:
        return f"Recette avec ID {recipe_id} supprimée avec succès."
    else:
        return f"Aucune recette trouvée avec ID {recipe_id}."

### 2 - configuration de l'agent sans outils pour l'instant (étape 1) ###
system_prompt = "Tu es un assistant de cuisine virtuel. Tu aides les utilisateurs à gérer leurs recettes de cuisine et à créer de nouvelles recettes en bases de données. Mais tu peux aussi parler de tout au besoin . Sois amical et serviable."
agent = create_agent(llm, tools=[list_recipes_tool, create_recipe_tool, delete_recipe_tool], system_prompt=system_prompt)
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
   

    return ChatResponse(
        ### 4 - retourner la réponse du modèle (étape 1) ###
        
        reply=result["messages"][-1].content # attention à la structure de la réponse content et pas ["content"]
    )
