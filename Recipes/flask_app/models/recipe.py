from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class Recipe:
    db = "recipes_schema"
    def __init__(self,data) -> None:
        self.id = data["id"]
        self.name = data["name"]
        self.under30 = data["under30"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_made_on = data["date_made_on"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        
        

    @classmethod
    def createRecipe(cls,data):
        query = "INSERT INTO recipes (name,under30,description,instructions,date_made_on, created_at,updated_at) VALUES (%(name)s,%(under30)s,%(description)s,%(instructions)s,%(date_made_on)s,NOW(),NOW());"
        return connectToMySQL(cls.db).query_db(query,data)
        

    @classmethod
    def getAllByUserId(cls,data):
        query = "SELECT * FROM recipes AS r LEFT JOIN users AS u ON u.id = r.user_id WHERE u.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        recipes = []
        if not results:
            recipes = []
        else:
            for row in results:
                recipes.append(cls(row))
        return recipes

    @classmethod
    def getAllRecipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for r in results:
            recipes.append(cls(r))
        return recipes

    @classmethod
    def getOneRecipeByUserId(cls,id):
        query = "SELECT * FROM recipes AS r LEFT JOIN users AS u ON u.id = r.user_idWHERE u.id = %(id)s ORDER BY r.id LIMIT 1);"
        data = {
            "id": id
        }
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def updateRecipe(cls,data):
        query = "UPDATE TABLE recipes SET name = %(name)s,under30minutesYesOrNo = %(under30minutesYesOrNo)s,description = %(description)s,instructions = %(instructions)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod 
    def deleteRecipe(cls,id):
        query = "DELETE FROM recipes WHERE id = %(id)s;" 
        data = {
            "id": id
        }
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validateRecipe(recipe):
        isValid = True
        if len(recipe["name"]) < 3:
            flash("Recipe name cannot be blank and must have at least 3 characters.")
            isValid = False
        if len(recipe["description"]) < 3:
            flash("Description cannot be blank and must have at least 3 characters.")
            isValid = False
        if len(recipe["instructions"]) < 3:
            flash("Instructions cannot be blank and must have at least 3 characters.")
        if not recipe["date_made_on"]:
            isValid = False
            flash("Must set data")
        return isValid
