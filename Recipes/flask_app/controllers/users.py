from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models import user, recipe

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register/user",methods=["POST"])
def registerUser():
    if not user.User.validateRegistration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # because of hashed password, we can't pass on the data directly from request.form to our database
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    session['id'] = user.User.saveUser(data)
    if not user.User.getUserByEmail(request.form["email"]):
        return redirect("/")
    return redirect('/dashboard')


@app.route("/login",methods=["POST"])
def login():
    if not user.User.validateLogin(request.form):
        return redirect("/")
    # see if user with email/username exists
    data = { "email": request.form["email"]}
    userVerify = user.User.getUserByEmail(data)
    if not userVerify:
        flash("invalid login")
        return redirect("/")
    if not bcrypt.check_password_hash(userVerify.password, request.form["password"]):
        flash("Wrong password")
        return redirect("/")
    session["id"] = userVerify.id
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "id" not in session:
        return redirect("/")
    data = {
        "id": session["id"]
    }
    userI = user.User.getUserById(data)
    recipes = recipe.Recipe.getAllRecipes()
    return render_template("dashboard.html", user = userI, recipes = recipes)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")