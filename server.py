import flask
from flask import Flask, request, redirect, render_template, flash
# import requests
import random
from models.api_connection import name_get, ingredient_get, id_get, random_recipe
from models.user import get_user, is_authenticated, generate_password_hash, password_valid, already_signup, create_new_user, get_userid
from models.recipes import get_my_recipes, get_popular_recipes, insert_recipe, delete_recipe_data, get_recipe, update_recipe_data

app = Flask(__name__)
app.secret_key = b'top_secret'

def render_template(template_name, **context):
    username = context.pop("username", None)
    username = username or request.cookies.get('name')
    return flask.render_template(template_name, username=username, **context)

@app.route('/', methods = ['GET'])
def favourite_drinks():
    resp = get_popular_recipes()
    username = request.cookies.get('name')
    if username != None:
        my_recipes = get_my_recipes([username])
        my_recipes_name = [my_recipe[0] for my_recipe in my_recipes]
        return render_template('index.html', recipes = resp, my_recipes = my_recipes_name)
    return render_template('index.html', recipes = resp)

@app.route('/search_name', methods=['POST'])
def search_by_name():
    drink = request.form.get('drink')
    # response = requests.get(f'https://thecocktaildb.com/api/json/v1/1/search.php?s={drink}')
    # resp = response.json()['drinks'][0]
    # id = resp.idDrink
    resp = name_get(drink)
    print (resp)
    if resp == None:
        flash('No drinks can be found. Please enter another coctail.')
        return redirect('/')
    else: 
        resp = resp[0]
        id = resp['idDrink']
        return redirect(f'/drinks/{id}')

@app.route('/search_ingredient', methods=['POST'])
def search_by_ingredient():
    ingredient = request.form.get('ingredient')
    resp = ingredient_get(ingredient)
    print(resp)
    if resp is None:
        flash('No drink containing such ingredient can be found. Please enter another ingredient.')
        return redirect('/')

    resp.json()
    resp = resp.json()['drinks']
    randomlist = []
    for i in range(0,6):
        n = random.randint(1, len(resp))
        randomlist.append(resp[n])

    return render_template('drink_by_ingredient.html', drinks = randomlist, ingredient = ingredient)

@app.route('/search_random', methods = ['POST'])
def random_search():
    resp = random_recipe()
    id = resp['idDrink']
    return redirect(f'/drinks/{id}')

@app.route('/drinks/<drink_id>', methods = ['GET'])
def ingredient_detail(drink_id):
    # 1. fetch the recipe
    # 2. populate the 'notes' for this user
    #    if they exist.
    username = request.cookies.get('name')
    id, name, image, ingredients, instructions = id_get(drink_id)
    if username != None: 
        userid = get_userid([username])
        resp = get_recipe([drink_id, userid])
        if resp != None: 
            return redirect(f'/edit_recipe/{drink_id}')
        else: 
            return render_template('drink.html', ingredients = ingredients, instructions = instructions, id = id, name = name, image = image, userid = userid)
    return render_template('drink.html', ingredients = ingredients, instructions = instructions, id = id, name = name, image = image)

@app.route('/add_recipe_action', methods = ['POST'])
def add_recipe_action():
    user_id = request.form.get('user_id')
    drink_id = request.form.get('id')
    drink_name = request.form.get('name')
    drink_url = request.form.get('image')
    drink_url = drink_url + '/preview'
    notes = request.form.get('notes')
    rating = request.form.get('rating')
    print (drink_id, drink_name, drink_url, notes, rating, user_id)

    insert_recipe([notes, rating, drink_name, drink_id, drink_url, user_id])
    return redirect('/my_recipes')


@app.route('/my_recipes')
def my_notes():
    my_name = request.cookies.get('name')
    resp = get_my_recipes([my_name])
    return render_template('my_recipes.html', recipes = resp)

@app.route('/login', methods = ['GET'])
def login():
    return render_template('login.html')


@app.route('/login_action', methods=['POST', 'GET'])
def login_action():
    email = request.form.get('email')
    password = request.form.get('password')
    name, password_hash = get_user(email)
    
    if password_valid(password, password_hash):
    # print(email)
        response=redirect('/')
        response.set_cookie('name', name)
        return response
    else: 
        flash('Email address or password is incorrect')
        return redirect('/login')


@app.route('/logout_action', methods=['POST'])
def logout_action():
    response = redirect('/')
    response.delete_cookie('name')
    return response

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/signup_action', methods = ['POST'])
def signup_action():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if already_signup(email):
        return redirect('/login')
    else:
        password_hass = generate_password_hash(password)
        create_new_user([email, name, password_hass])
        return redirect('/')

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    username = request.cookies.get('name')
    userid = get_userid([username])
    resp = get_recipe([recipe_id, userid])
    return render_template('delete_recipe.html', resp = resp)
    
@app.route('/delete_recipe_action', methods = ['POST'])
def delete_recipe_action():
    id = request.form.get('id')
    delete_recipe_data([id])
    return redirect('/my_recipes')


@app.route('/edit_recipe/<recipe_id>', methods=['GET'])
# 1. fetch the recipe
# 2. populate the 'notes' for this user
#    if they exist.
def edit_recipe(recipe_id):
    username = request.cookies.get('name')
    userid = get_userid([username])

    resp = get_recipe([recipe_id, userid])
    id, name, image, ingredients, instructions = id_get(recipe_id)

    return render_template('edit_recipe.html', ingredients = ingredients, instructions = instructions, id = id, name = name, image = image, resp = resp)

@app.route('/edit_recipe_action', methods = ['POST'])
def update_recipe():
    id = request.form.get('id')
    notes = request.form.get('notes')
    rating = request.form.get('rating')
    update_recipe_data([notes, rating, id])
    return redirect('/my_recipes')

if __name__ == '__main__':
    app.run(debug=True, port=5005)