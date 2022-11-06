from flask import Flask, request, redirect, render_template
import requests
import random
from models.api_connection import name_get, ingredient_get, id_get

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def favourite_drinks():
    return render_template('index.html')

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
    id, name, image, ingredients, instructions = id_get(drink_id)
    return render_template('drink.html', ingredients = ingredients, instructions = instructions, id = id, name = name, image = image)

@app.route('/my_notes')
def my_notes():
    return render_template('my_notes.html')


app.run(debug=True)