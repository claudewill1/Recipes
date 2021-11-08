from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import recipe,user
from flask_app import app
CONST_DASHBOARD = "/dashboard"
@app.route("/dashboard/<int:id>/newRecipe")
def createRecipe(id):
    userById = user.User.getUserById(id)
    return render_template("add.html", user = userById)

@app.route("/recipes/new/create", methods=["POST"])
def create_new():
    if not recipe.Recipe.validateRecipe(request.form):
        return redirect("/dashboard/<int:id>/newRecipe")
    data = {
        "name": request.form['name'],
        "under30": request.form["under30"],
        "description": request.form['description'],
        "instructions": request.form["instructions"],
        "date_made_on": request.form["date_made_on"]
    }
    recipe.Recipe.createRecipe(data)
    return redirect(CONST_DASHBOARD)

@app.route('/recipes/view/<int:recipe_id>')
def showRecipe(recipe_id):
    this_recipe = recipe.Recipe.getRecipeById({'id': recipe_id})
    this_user = user.User.getUserById({'id': session['id']})

    return render_template('show.html', recipe = this_recipe, user = this_user)

@app.route("/recipes/edit/<int:id>")
def editRecipe(id):
    return render_template("edit.html",recipe = recipe.Recipe.getRecipeById({"id": id}),user = user.User.getUserById({"id": session["id"]}))

@app.route("/recipes/update/<int:recipe_id>",methods=["POST"])
def updateRecipe(recipe_id):
    if not recipe.Recipe.validateRecipe(request.form):
        return redirect(url_for('.editRecipe', recipe_id = recipe_id))
    data = {
        "id": recipe_id,
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under30": request.form["under30"],
        "user_id": session["id"]
    }
    recipe.Recipe.updateRecipe(data)
    return redirect(CONST_DASHBOARD)

@app.route("/recipes/delete/<int:id>")
def deleteRecipe(id):
    recipe.Recipe.deleteRecipe(id)
    return redirect(CONST_DASHBOARD)
    