"""Store en mémoire pour les recettes. Pas de persistence — repart de zéro à chaque démarrage."""

from itertools import count

from pydantic import BaseModel


class Recipe(BaseModel):
    id: int
    name: str
    ingredients: list[str]


class RecipeCreate(BaseModel):
    name: str
    ingredients: list[str]


_id_counter = count(start=1)
_recipes: dict[int, Recipe] = {}


def list_recipes() -> list[Recipe]:
    return list(_recipes.values())


def get_recipe(recipe_id: int) -> Recipe | None:
    return _recipes.get(recipe_id)


def create_recipe(data: RecipeCreate) -> Recipe:
    new_id = next(_id_counter)
    recipe = Recipe(id=new_id, name=data.name, ingredients=data.ingredients)
    _recipes[new_id] = recipe
    return recipe


def delete_recipe(recipe_id: int) -> bool:
    return _recipes.pop(recipe_id, None) is not None


create_recipe(RecipeCreate(
    name="Tarte aux pommes",
    ingredients=["pommes", "pâte brisée", "sucre", "cannelle"],
))
create_recipe(RecipeCreate(
    name="Quiche lorraine",
    ingredients=["pâte brisée", "lardons", "œufs", "crème fraîche"],
))
