"""Routes for our flask app"""
from flask import request
from .data_loader import DataLoader
from . import app
#Flask Routes

#Set Up Data stuff
loader = DataLoader()

recipes = loader.load()
#GET

@app.get("/recipes")
def get_recipe_names(current_recipes = recipes):
    """Gets all recipes"""
    response = list(current_recipes.keys())
    return {"recipeNames": response}

@app.get("/hello")
def hello():
    return 'hello world!',200
    
@app.get("/recipes/details/<name>")
def get_recipe(name,current_recipes = recipes):
    """Gets specific recipe"""
    if name in current_recipes:
        recipe = current_recipes[name]
        return {"details":recipe}, 200
    return "", 200

#POST

@app.post("/recipes")
def post_recipes(current_recipes = recipes,current_loader=loader):
    """Post a new recipe"""
    data = request.get_json(force=True)
    # We make a backup here, incase something happens
    # while we are writing the data to the JSON,
    # in which case we will roll back to the origional state of the dict
    # to avoid the two being out of sync
    backup_recipes = current_recipes.copy()
    if data.get("name") in current_recipes:
        return {"error":"Recipe already exists"},400
    try:
        current_recipes[data.get("name")]={"ingredients":data.get("ingredients"),
                                   "instructions":data.get("instructions")}
        current_loader.write(current_recipes)
    except Exception:
        # we dont really care what the exception is
        # we're just gonna roll it back, and return a 500
        current_recipes = backup_recipes
        return {"error": "Error writing, rolling back"}, 500
    return "", 204

#PUT

@app.put("/recipes")
def update_recipe(current_recipes = recipes,current_loader=loader):
    """update an existing recipe"""
    data = request.get_json(force=True)
    # We make a backup here, incase something happens
    # while we are writing the data to the JSON,
    # in which case we will roll back to the origional state of the dict
    # to avoid the two being out of sync
    backup_recipes = current_recipes.copy()
    if data.get("name") not in recipes:
        return {"error": "Recipe doesn't exist"}, 404
    try:
        current_recipes[data.get("name")]["ingredients"] = data.get("ingredients")
        current_recipes[data.get("name")]["instructions"] = data.get("instructions")
        current_loader.write(current_recipes)
    except Exception:
        # we dont really care what the exception is
        # we're just gonna roll it back, and return a 500
        current_recipes = backup_recipes
        return {"error": "Error writing, rolling back"}, 500

    return "", 204

#DELETE

@app.delete("/recipes")
def delete_recipe(current_recipes = recipes,current_loader=loader):
    data = request.get_json(force=True)
    if data.get("name") not in recipes:
        return {"error": "Recipe doesn't exist"}, 404
    try:
        del current_recipes[data.get("name")]
    except Exception:
        return {"error": "Error writing, rolling back"}, 500
    return {"deleted":  data.get("name")}, 200
    
