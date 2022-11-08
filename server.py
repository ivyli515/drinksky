from flask import Flask, request, redirect, render_template
import requests
import random
from models.api_connection import name_get, ingredient_get, id_get
from models.user import get_user, is_authenticated, generate_password_hash, password_valid, already_signup, create_new_user, get_my_recipes, get_popular_recipes, get_userid

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def favourite_drinks():
    name = request.cookies.get('name')
    resp = get_popular_recipes()
    return render_template('index.html', recipes = resp, username = name)

@app.route('/search_name', methods=['POST'])
def search_by_name():
    drink = request.form.get('drink')
    # response = requests.get(f'https://thecocktaildb.com/api/json/v1/1/search.php?s={drink}')
    # resp = response.json()['drinks'][0]
    # id = resp.idDrink
    resp = name_get(drink)
    id = resp['idDrink']
    return redirect(f'/drinks/{id}')

@app.route('/search_ingredient', methods=['POST'])
def search_by_ingredient():
    ingredient = request.form.get('ingredient')
    resp = ingredient_get(ingredient)
    randomlist = []
    for i in range(0,6):
        n = random.randint(1, len(resp))
        randomlist.append(resp[n])

    return render_template('drink_by_ingredient.html', drinks = randomlist, ingredient = ingredient)


@app.route('/drinks/<drink_id>')
def ingredient_detail(drink_id):
    # 1. fetch the recipe
    # 2. populate the 'notes' for this user
    #    if they exist.
    username = request.cookies.get('name')
    userid = get_userid(username)
    id, name, image, ingredients, instructions = id_get(drink_id)
    return render_template('drink.html', ingredients = ingredients, instructions = instructions, id = id, name = name, image = image, userid = userid)

# @app.route('/add_drink_action')
# def add_drink_action():
#     pass


@app.route('/my_recipes')
def my_notes():
    my_name = request.cookies.get('name')
    resp = get_my_recipes()
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

# @app.route('/delete_drink')
# def delete_drink():
#     pass

# @app.route('/delete_drink_action')
# def delete_drink():
#     pass

# @app.route('/edit_drink')
# def edit_drink():
#     pass

if __name__ == '__main__':
    app.run(debug=True, port=5005)