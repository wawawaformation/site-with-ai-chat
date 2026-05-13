"""Routes CRUD pour les recettes — déjà implémentées, à étudier comme exemple."""

from fastapi import APIRouter, HTTPException

from app.store import (
    Recipe,
    RecipeCreate,
    create_recipe,
    delete_recipe,
    get_recipe,
    list_recipes,
)

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("", response_model=list[Recipe])
def get_all_recipes() -> list[Recipe]:
    return list_recipes()


@router.get("/{recipe_id}", response_model=Recipe)
def get_one_recipe(recipe_id: int) -> Recipe:
    recipe = get_recipe(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recette introuvable")
    return recipe


@router.post("", response_model=Recipe, status_code=201)
def post_recipe(data: RecipeCreate) -> Recipe:
    return create_recipe(data)


@router.delete("/{recipe_id}", status_code=204)
def remove_recipe(recipe_id: int) -> None:
    if not delete_recipe(recipe_id):
        raise HTTPException(status_code=404, detail="Recette introuvable")
