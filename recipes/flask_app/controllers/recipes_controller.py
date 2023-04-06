# ==== ROUTING  ====
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe_model import Recipe


#  ================== Add a New Recipe!  CREATE page    - VIEW
@app.route('/recipes/new')
def new_recipe():
    return render_template("recipe_new.html")


#  ===================  CREATE  - ACTION  method (POST)
@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    print(f"-------{request.form}---------")
#  validate the model
    if not Recipe.validator(request.form):
        return redirect("/recipes/new")
    recipe_data = {
        **request.form,
        'user_id': session['user_id']
    }
    Recipe.create(recipe_data)
    return redirect('/dashboard')


#  ============    UPDATE  - EDIT PAGE  ========
@app.route('/recipes/<int:id>/edit')
def edit_recipe(id):

    data = {
        "id": id
    }
    this_recipe = Recipe.get_by_id(data)
    return render_template("recipe_edit.html",
                            this_recipe = this_recipe)


#  ===================  UPDATE   - ACTION  method (POST)
@app.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    #  validate the model
    if not Recipe.validator(request.form):
        return redirect(f"/recipes/{id}/edit")
    
    data = {
        'id' : id,
        **request.form
    }
    
    Recipe.update(data)
    return redirect('/dashboard')



#  =============  READ ONE  show   ============
@app.route("/recipes/<int:id>")
def show_one_recipe(id):
    this_recipe = Recipe.get_by_id({'id': id})
    return render_template("recipe_one.html",
                            this_recipe = this_recipe)
    



#  =================    DELETE     ============
@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    Recipe.delete({'id' : id})
    return redirect('/dashboard')
