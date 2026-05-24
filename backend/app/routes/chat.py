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
import random
from dotenv import load_dotenv

from fastapi import APIRouter
from pydantic import BaseModel
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig


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
    
@tool
def flatter_utilisateur_tool() -> str:
    """Outil pour flatter l'utilisateur."""
    flatteries = [
        "Tu es vraiment un chef incroyable !",
        "Tes compétences culinaires sont impressionnantes !",
        "Tu as un talent naturel pour la cuisine !",
        "Tes recettes sont toujours délicieuses !",
        "Tu es une source d'inspiration en cuisine !"
    ]
    return random.choice(flatteries)
    
    


@tool
def miauler_tool() -> str:
    """Outil pour miauler comme un chat."""
    return "Miaou !"


### 3 - configuration de l'agent avec outils (étape 2)  et sauvegarde de session (etape 3)###

system_prompt = """
Tu aides les utilisateurs à gérer leurs recettes de cuisine :
- lister les recettes existantes ;
- créer une nouvelle recette ;
- supprimer une recette par identifiant.

Tu peux aussi discuter de cuisine de manière générale.

Tu as le droit d'avoir un ton humoristique, mais l'humour doit rester léger,
bienveillant et ne doit pas viser une personne réelle de manière blessante.

Quand une action nécessite un outil, utilise l'outil adapté.
Quand il manque une information nécessaire, pose une question de clarification.

"""

checkpointer = InMemorySaver()

agent = create_agent(
    llm, 
    tools=[
        list_recipes_tool, 
        create_recipe_tool, 
        delete_recipe_tool, 
        flatter_utilisateur_tool,
        miauler_tool
    ],
    system_prompt=system_prompt,
    checkpointer=checkpointer
)
router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"


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
