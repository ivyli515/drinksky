from .database import sql_select_all, sql_write, sql_select_one

def get_my_recipes():
    results = sql_select_all("SELECT recipes.drink_name, recipes.drink_id, recipes.drink_url, recipes.rating FROM recipes INNER JOIN users ON recipes.user_id = users.id WHERE users.name = 'Ivy' ORDER BY recipes.rating DESC", [])
    return results

def get_popular_recipes():
    results = sql_select_all("SELECT recipes.drink_name, recipes.drink_id, recipes.drink_url FROM recipes INNER JOIN users ON recipes.user_id = users.id GROUP BY recipes.drink_name, recipes.drink_id, recipes.drink_url ORDER BY COUNT(users.id) DESC",[])
    return results

def insert_recipe(parameters):
    sql_write('INSERT INTO recipes (notes, rating, drink_name, drink_id, drink_url, user_id) VALUES (%s, %s, %s, %s, %s, %s)', parameters)
    return