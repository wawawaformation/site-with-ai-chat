"""
Creation et configuration de l'agent

"""


from langchain.agents import create_agent


from langgraph.checkpoint.memory import InMemorySaver
from app.agent.tools import *
from app.agent.llm_infomaniak_apertus import llm

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