"""
Tools de l'agent
    
"""

from app.store import list_recipes, create_recipe, delete_recipe, RecipeCreate
from langchain.tools import tool
import random



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