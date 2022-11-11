import requests

def name_get(name):
    resp = requests.get(f'https://thecocktaildb.com/api/json/v1/1/search.php?s={name}')
    resp = resp.json()['drinks']
    return resp

def ingredient_get(ingredient):
    resp = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={ingredient}')
    # Sometimes the response for a not found ingredient is just an empty string
    # and that causes calls to .json() to encoutner encoding issues.
    if resp.text == '':
        return None
    return resp

def random_recipe():
    response = requests.get('http://www.thecocktaildb.com/api/json/v1/1/random.php')
    resp = response.json()['drinks'][0]
    return resp

def id_get(id):
    response = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={id}')
    resp = response.json()['drinks'][0]
    id = resp['idDrink']
    name = resp['strDrink']
    image = resp['strDrinkThumb']
    i = 1
    ingredients = []
    while resp[f'strIngredient{i}'] != None:
        if resp[f'strMeasure{i}'] == None:
            resp[f'strMeasure{i}'] = ''
        ingredient = resp[f'strMeasure{i}'] + ' ' + resp[f'strIngredient{i}']
        ingredients.append(ingredient)
        i += 1
    instructions = resp['strInstructions']
    return id, name, image, ingredients, instructions