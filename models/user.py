import bcrypt
from .database import sql_select_all, sql_select_one, sql_write

def get_user(email):
    results = sql_select_one('SELECT name, password_hash FROM users WHERE email=%s', [email])
    name = results[0]
    hash = results[1]
    return name, hash

def is_authenticated(request) -> bool:
    """
    Check cookie in request for authentication.  Does
    not check that the user exists.
    """
    return bool(request.cookies.get("name"))

def generate_password_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def password_valid(password, password_hash):
    return bcrypt.checkpw(password.encode(), password_hash.encode())

def already_signup(email):
    results = sql_select_one('SELECT id FROM users WHERE email = %s', [email])
    if results:
        return True
    else: return False

def create_new_user(parameters):
    sql_write('INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)', parameters)
    return 

def get_my_recipes():
    results = sql_select_all("SELECT recipes.drink_name, recipes.drink_id, recipes.drink_url, recipes.rating FROM recipes INNER JOIN users ON recipes.user_id = users.id WHERE users.name = 'Ivy' ORDER BY recipes.rating DESC", [])
    return results

def get_popular_recipes():
    results = sql_select_all("SELECT recipes.drink_name, recipes.drink_id, recipes.drink_url FROM recipes INNER JOIN users ON recipes.user_id = users.id GROUP BY recipes.drink_name, recipes.drink_id, recipes.drink_url ORDER BY COUNT(users.id) DESC",[])
    return results

def get_userid(parameter):
    results = sql_select_one('SELECT id FROM users WHERE name = %s', [parameter])
    return results