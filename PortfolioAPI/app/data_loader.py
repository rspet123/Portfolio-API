"""data loaders and other data interacting functions for interacting with the json file"""
import json
import os
class DataLoader:
    """Set of functions to help loading and unloading data"""
    dirname = os.path.dirname(__file__)
    recipe_path = (dirname+"\\recipes.json")

    #our overloaded constructor, to make sure we can do other stuff, not just recipes


    @classmethod
    def load(cls):
        """Loads JSON file to a dict"""
        recipe_dict = {}
        with open(cls.recipe_path,"r") as data_file:
            recipe_list = json.load(data_file).get("recipes")
        #It gives us a list, which is okay
        #but we kind of want it to be faster, and we want to be able to find
        #recipies quickly, without having to iterate through the list
        #So I'll turn it into a dict
        for recipe in recipe_list:
            recipe_dict[recipe["name"]] = {"ingredients":recipe["ingredients"],
                                           "instructions":recipe["instructions"]}
        return recipe_dict

    # Simply updates the recipe on the dict, but does not *save* it
    # or write it to the disk
    @classmethod
    def update_recipe(cls, recipe: dict, updated_recipe: dict):
        """Update Recipe"""
        for key, val in updated_recipe.items():
            recipe[key] = val

    # Helper method to allow us to turn the dict that we made when loading
    # back into a list, to allow us to save it on the disk
    # exactly how it was
    @staticmethod
    def recipe_dict_to_list(recipe_dict: dict):
        """Helper Method, dict -> List"""
        recipe_list =[]
        for recipe_name in recipe_dict.keys():
            recipe_list.append({"name":recipe_name,
             "ingredients":recipe_dict[recipe_name]["ingredients"],
             "instructions":recipe_dict[recipe_name]["instructions"]
             })
        return recipe_list
    # we use this to write to disk
    @classmethod
    def write(cls, recipe_dict: dict):
        """Write Dict to disk"""
        recipe_list = cls.recipe_dict_to_list(recipe_dict)
        with open(cls.recipe_path, "w") as data_file:
            json.dump({"recipes": recipe_list}, data_file, indent=2)
            