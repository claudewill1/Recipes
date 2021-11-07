from flask import render_template, redirect, request, session, flash
from flask_app.models import recipe,user
from flask_app import app

@app.route("/dashboard/<int:id>/newRecipe")
def createRecipe(id):
    userById = user.User.getUserById(id)
    return render_template("add.html", user = userById)

@app.route("/recipes/new/create", methods=["POST"])
def create_new():
    data = {
        "name": request.form['name'],
        "under30": request.form["under30"],
        "description": request.form['description'],
        "instructions": request.form["instructions"],
        "date_made_on": request.form["date_made_on"]
    }
    recipe.Recipe.createRecipe(data)
    return redirect("/dashboard")

#@app.route("/addRecipe",methods=["POST"])
#def addRecipe():
 #   data = {
  ##     'description': request.form['description'],
  #      'instructions': request.form['instructions'],
   #     'date_made_on' : request.form['date_made_on'],
   #     'under30': request.form['under30'],
   ##  }

    

   # if recipe.Recipe.validateRecipe(data):
   #     id = recipe.Recipe.createRecipe(data)
   #     return redirect(f'/dashboard/{data["user_id"]}')

  #  return redirect(f'/dashboard/{data["user_id"]}/newRecipe')
    