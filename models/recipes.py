from .database import sql_select_all, sql_write, sql_select_one

def get_my_recipes(parameter):
    results = sql_select_all("SELECT recipes.drink_name, recipes.drink_id, recipes.drink_url, recipes.rating FROM recipes INNER JOIN users ON recipes.user_id = users.id WHERE users.name = %s ORDER BY recipes.rating DESC", parameter)
    return results

def get_popular_recipes():
    results = sql_select_all("SELECT recipes.drink_name, recipes.drink_id, recipes.drink_url, COUNT(users.id) FROM recipes INNER JOIN users ON recipes.user_id = users.id GROUP BY recipes.drink_name, recipes.drink_id, recipes.drink_url ORDER BY COUNT(users.id) DESC",[])
    return results

def insert_recipe(parameters):
    sql_write('INSERT INTO recipes (notes, rating, drink_name, drink_id, drink_url, user_id) VALUES (%s, %s, %s, %s, %s, %s)', parameters)
    return

def delete_recipe_data(parameter):
    sql_write('DELETE FROM recipes WHERE id = %s', parameter)
    return 

def get_recipe(parameters):
    results = sql_select_one("SELECT * FROM recipes WHERE drink_id=%s AND user_id = %s", parameters)
    return results

def update_recipe_data(parameters):
    sql_write('UPDATE recipes SET notes=%s, rating=%s WHERE id = %s', parameters)
    return 