import flask_unittest
from flask import Flask
from app import app

class TestAPI(flask_unittest.ClientTestCase):
    # Assign the flask app object
    
    app = app
    def test_hello_world(self, client):
        response = client.get('/hello')
        status_code = response.status_code
        response_text = (response.data).decode('utf-8')
        self.assertEqual(status_code, 200)
        self.assertEqual(response_text, 'hello world!')
        
    def test_get_recipes(self, client):
        expected = """{"recipeNames":["scrambledEggs","garlicPasta","chai"]}\n"""
        response = client.get('/recipes')
        status_code = response.status_code
        response_data = response.data.decode('utf-8')
        self.assertEqual(status_code, 200)
        self.assertEqual(response_data, expected)
        
    def test_post_recipes(self, client):
        post_req = """
    {
      "name": "waffles",
      "ingredients": [
        "waffle batter"
      ],
      "instructions": [
        "cook it"
      ]
    }
    """
        expected = """{"recipeNames":["scrambledEggs","garlicPasta","chai","waffles"]}\n"""
        response_1 = client.post("/recipes",data=post_req)
        
        response_2 = client.get('/recipes')
        status_code = response_1.status_code
        response_data = response_2.data.decode('utf-8')
        self.assertEqual(status_code, 204)
        self.assertEqual(response_data, expected)
        
    def test_delete_recipes(self, client):
        post_req_1 = """
    {
      "name": "waffles",
      "ingredients": [
        "waffle batter"
      ],
      "instructions": [
        "cook it"
      ]
    }
    """
        post_req_2 = """
    {
      "name": "pancakes",
      "ingredients": [
        "pancake batter"
      ],
      "instructions": [
        "cook it"
      ]
    }
    """
        response_1 = client.delete("/recipes",data=post_req_1)
        self.assertEqual(response_1.status_code,200)
        self.assertEqual(response_1.data.decode('utf-8'),"""{"deleted":"waffles"}\n""")
        response_2 = client.delete("/recipes",data=post_req_2)
        self.assertEqual(response_2.status_code,404)