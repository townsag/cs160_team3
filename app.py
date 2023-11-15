import db
from groute import grouteInputOrder, grouteResponse, plan_path, distance_check
import json
from functools import wraps
import threading
from flask import Flask, request, send_from_directory
from flask_login import LoginManager, login_user, logout_user, current_user

import pdb
import configparser

config = configparser.ConfigParser()
config.read('.env')
API_KEY = config['KEYS']['GOOGLE_ROUTES_API_KEY']
PLACES_API_KEY = config['KEYS']['GOOGLE_PLACES_API_KEY']
ORIGIN = "1 Washington Sq, San Jose, CA 95192"



login_manager = LoginManager()
app = Flask(__name__, static_folder='ogo/dist')
app.secret_key = b'replace_this_later'  # TODO: use enviroment variable instead

login_manager.init_app(app)
login_manager.login_view = "login"


class User:
  def __init__(self, user_id, username, address, is_admin):
    self.user_id = user_id
    self.username = username
    self.address = address
    self.is_admin = is_admin

  def get_id(self):
    return str(self.user_id)

  @property 
  def is_authenticated(self):
    return True

  @property
  def is_active(self):
    return True


  @property
  def is_anonymous(self):
    return False

  @staticmethod
  def get(user_id):
    try:
      u = db.select_user(user_id)
      return User(user_id, u['username'], u['address'], u['is_admin'])
    except Exception as e:
      print('User.get() error:', e)
      return None
    

@login_manager.user_loader
def load_user(user_id):
  return User.get(user_id)


# Flask route decorator to require the request to be made by a logged in user.
def login_required(f):
    @wraps(f)
    def check_login(*args, **kwargs):
        if not current_user.is_authenticated:
            return "Unauthorized: You must be logged in to use this route.", 401
        return f(*args, **kwargs)
    return check_login


# Flask route decorator to require the request to be made by a logged in admin user.
def admin_required(f):
    @wraps(f)
    def check_admin(*args, **kwargs):
        if not current_user.is_authenticated:
          return "Unauthorized: You must be logged in to use this route.", 401
        if not current_user.is_admin:
            return "Unauthorized: You must be logged in as admin to use this route.", 401
        return f(*args, **kwargs)
    return check_admin


def get_item_in_cart(product_id : int):
  curr_cart = db.select_cart(current_user.user_id)
  for item in curr_cart['items']:
    if item['product_id'] == product_id:
      return item
  return None


def is_valid_product_id(product_id : int):
  if db.select_product(product_id) == None:
    return False
  return True

def is_valid_category_id(category_id : int):
  if db.select_category(category_id) == None:
    return False
  return True

def is_valid_tag(tag_id):
  tags = db.select_all_tags()
  for tag in tags:
    if tag['tag_id'] == tag_id:
      return True
  return False

def is_valid_cart_item_params(ci : json):
  if not isinstance(ci['quantity'], int):
    return False, ("Invalid quantity type", 400)
  if not isinstance(ci['product_id'], int):
    return False, ("Invalid productID type", 400)

  curr_cart = db.select_cart(current_user.user_id)
  cart_item = get_item_in_cart(ci["product_id"])
  if cart_item != None:
    ci['quantity'] = ci['quantity'] + cart_item['quantity']
  # if ci['quantity'] > 20:
  #   return False, ("requested product quantity is too high", 400)
  return True

def calculate_total_cart_weights(order_items : json):
  total_cart_weight = 0
  for order_item in order_items:
    product = db.select_product(order_item['product_id'])
    total_cart_weight = total_cart_weight + (product["weight"] * order_item["quantity"])
  return total_cart_weight

def is_valid_product_params(p : json):
    # name, description, image need to be string
  # Link must be a valid link
  # quantity, price, weight need to be type Integer
  # quantity, price, weight cannot be < 0 
  if not isinstance(p['name'], str):
    return False, ("Invalid name type", 400)
  if not isinstance(p['description'], str):
    return False, ("Invalid description type", 400)
  if not isinstance(p['image'], str):
    return False, ("Invalid image link type", 400)
  if not isinstance(p['quantity'], int):
    return False, ("Invalid quantity type", 400)
  if not isinstance(p['price'], float) and not isinstance(p['price'], int):
    return False, ("Invalid price type", 400)
  if not isinstance(p['weight'], float) and not isinstance(p['weight'], int):
    return False, ("Invalid weight type", 400)
  if not isinstance(p['quantity'], int):
    return False, ("Invalid name type", 400)
  if p['quantity'] < 0 or p['weight'] < 0 or p['price'] < 0:
    return False, ("Cannot have negative weight, price, or quantity", 400)
  if not is_valid_category_id(p['category_id']):
    return False, ("Category of that ID does not exist", 400)
  else:
    return True


def route_if_ready():
  print("started route if ready thread")
  # 
  # pdb.set_trace()
  batch = db.get_path_planning_batch()
  print("this is batch: ", batch)
  if batch == None:
    print("no path yet")
    return
  
  gresp: grouteResponse = plan_path([grouteInputOrder(o['order_id'], o['address']) for o in batch])

  legs = [{"order_id": l.order_id, "sequence": l.index, "eta": l.eta, "lat": l.lat, "lon": l.lon} for l in gresp.legs]
  db.insert_route(gresp.polyline, legs)
  print("inserted route!")


# #
# # Serve Static Files
# #
@app.route('/', methods=["GET"])
def root():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>', methods=["GET"])
def assets(path):
    try:
        response = send_from_directory(app.static_folder, path)
        return response
    except:
        return send_from_directory(app.static_folder, 'index.html')


# #
# # User Authentication Routes
# #
@app.route('/signup', methods=['POST'])
def signup():
  u = request.get_json()

  # If the user already exists log them in.
  j = db.validate_user(u['username'], u['password'])
  if j:
    l = load_user(j['user_id'])
    login_user(l)
    return 'Login Success'
  
  if 'is_admin' not in u: u['is_admin'] = False
  
  user_char_ct = len(u['username'])
  pass_char_ct = len(u['password'])
  if user_char_ct > 20 or user_char_ct < 1:
    return 'Invalid username character count', 400
  if pass_char_ct > 20 or pass_char_ct < 1:
    return 'Invalid password character count', 400
  if db.select_user_from_un(u['username']) != None:
    return 'Invalid username: already taken', 400
  u = db.insert_user(u['username'], u['password'], u['is_admin'])
  login_user(load_user(u['user_id']))  # Log the user in after they add their account to the db
  return 'Signup Success'
  # TODO: handle errors such as no key.


@app.route('/login', methods=['POST'])
def login():
  u = request.get_json()
  # print(u,"\n")
  j = db.validate_user(u['username'], u['password'])
  if j:
    login_user(load_user(j['user_id']))
    return 'Success'
  return 'Failure', 400


@app.route('/logout')
@login_required

def logout():
  msg = f"Logging out {current_user.username}"
  logout_user()
  return msg


# Do we allow multiple logins of an account on multiple pages? Potential race condition with updateUser
@app.route('/updateUser', methods=['POST'])
@login_required
def update_user():
  u = request.get_json()

  if 'username' in u:   
    stored_user_with_username = db.select_user_from_un(u['username'])
    if stored_user_with_username != None and stored_user_with_username['username'] != current_user.username:
      return "Invalid Entry - User Already Exists", 400
    user_char_ct = len(u['username'])
    if user_char_ct > 20 or user_char_ct < 1:
      return 'Invalid username character count', 400
    db.update_user_username(current_user.user_id, u['username'])

  if 'password' in u: 
    pass_char_ct = len(u['password'])
    if pass_char_ct > 20 or pass_char_ct < 1:
      return 'Invalid password character count', 400  
    db.update_user_password(current_user.user_id, u['password'])  
    
  if 'address' in u: 

    # Hitting Errors with Distance Check
    if not distance_check(u['address']): return 'Address invalid (bad format or too far).', 400
    
    db.update_user_address(current_user.user_id, u['address'])

  if 'is_admin' in u: 
    db.update_user_admin(current_user.user_id, u['is_admin'])

  return "Success", 200


@app.route('/getUser', methods=['GET'])
@login_required
def get_user():
  return {'user_id': current_user.user_id, 'username': current_user.username, 'address': current_user.address, 'is_admin': current_user.is_admin}


@app.route('/getAllUsers', methods=['GET'])
@admin_required
def get_all_users():
  return db.select_all_users()


@app.route('/demoteUser', methods=['POST'])
@admin_required
def demote_user():
  p = request.get_json()
  db.update_user_admin(p['user_id'], False)
  return "Success", 200


@app.route('/promoteUser', methods=['POST'])
@admin_required
def promote_user():
  p = request.get_json()
  db.update_user_admin(p['user_id'], True)
  return "Success", 200


# #
# # Product Routes
# #
@app.route('/getProducts', methods=['GET'])
@login_required
def get_products():
  return json.dumps(db.select_products())


@app.route('/getProduct', methods=['GET'])  # ?productID=<product_id>
@login_required
def get_product():
  product_id = request.args['productID']
  if not is_valid_product_id(product_id):
    return "Invalid Product ID, does not exist in current product list", 400  
  # TODO: handle if productID is not present in query string
  return json.dumps(db.select_product(product_id))


@app.route('/searchProducts', methods=['GET']) #?query=<query>
@login_required
def search_products():
  query = request.args['query']
  return json.dumps(db.search_products(query))


@app.route('/updateProduct', methods=['POST'])
@admin_required
def update_product():
  p = request.get_json()
  result = is_valid_product_params(p)
  if not isinstance(result, bool) or not result:
    return result[1]
  if not is_valid_product_id(p['product_id']):
    return "Invalid Product ID, does not exist in current product list", 400  
  return db.update_product(p['product_id'], p['name'], p['description'], p['image'], p['quantity'], p['price'], p['weight'], p['category_id'], p['tags'])


@app.route('/createProduct', methods=['POST'])
@admin_required
def create_product():
  p = request.get_json()
  result = is_valid_product_params(p)
  if not isinstance(result, bool) or not result:
    return result[1]
  return db.insert_product(p['name'], p['description'], p['image'], p['quantity'], p['price'], p['weight'], p['category_id'], p['tags'])


@app.route('/getCategories', methods=['GET'])
@login_required
def get_categories():
  return json.dumps(db.select_all_categories())


@app.route('/createCategory', methods=['POST'])
@admin_required
def create_category():
  p = request.get_json()
  return db.insert_category(p['name'])


@app.route('/updateCategory', methods=['POST'])
@admin_required
def update_category():
  p = request.get_json()
  if not is_valid_category_id(p["category_id"]):
    return "Invalid Category ID, does not exist in current category list", 400 
  return db.update_category(p['category_id'], p['name']) 


@app.route('/getTags', methods=['GET'])
@login_required
def get_tags():
  return json.dumps(db.select_all_tags())


@app.route('/createTag', methods=['POST'])
@admin_required
def create_tag():
  p = request.get_json()
  return db.insert_tag(p['name'])


@app.route('/updateTag', methods=['POST'])
@admin_required
def update_tag():
  p = request.get_json()
  if not is_valid_tag(p['tag_id']):
    return "Invalid Tag ID, does not exist in current tag list", 400
  return db.update_tag(p['tag_id'], p['name']) 

# #
# # Cart Routes
# #
@app.route('/getCart', methods=['GET'])
@login_required
def get_cart():
  return db.select_cart(current_user.user_id)



@app.route('/addCartItem', methods=['POST'])
@login_required
def add_cart_item():
  ci = request.get_json()
  if not is_valid_product_id(ci['product_id']):
    return "Invalid Product ID, does not exist in current product list", 400
  result = is_valid_cart_item_params(ci)
  if not isinstance(result, bool) or not result:
    return result[1]
  cart_item = get_item_in_cart(ci["product_id"])
  if cart_item != None:
    return db.update_cart_item(current_user.user_id, cart_item['cart_item_id'], ci['product_id'], ci['quantity'])
  else:
    return db.insert_cart_item(current_user.user_id, ci['product_id'], ci['quantity'])


@app.route('/updateCartItem', methods=['POST'])
@login_required
def update_cart_item():
  ci = request.get_json()

  if not isinstance(ci['quantity'], int):
    return "Invalid quantity type", 400
  if not isinstance(ci['product_id'], int):
    return "Invalid productID type", 400
  if not isinstance(ci['cart_item_id'], int):
    return "Invalid cartItemID type", 400
  
  if not is_valid_product_id(ci['product_id']):
    return "Invalid Product ID, does not exist in current product list", 400
  
  cart_item = get_item_in_cart(ci["product_id"])
  if cart_item == None:
    return "Product ID not currently in shopping cart", 400
  
  item_in_inventory = db.select_product(ci['product_id']) 
  if ci["quantity"] > item_in_inventory['quantity']:
    return "Not enough stock of item, \"" + item_in_inventory["name"] + "\". (Currently "+ str(item_in_inventory['quantity']) + " in stock)", 400 

  # curr_cart_items = db.select_cart(current_user.user_id)['items']
  # for index in range(len(curr_cart_items)):
  #   if curr_cart_items[index]['product_id'] == ci['product_id']:
  #     curr_cart_items[index]['quantity'] = ci['quantity']
  # if calculate_total_cart_weights(curr_cart_items) > 200:
  #   return "Order is too heavy to purchase. Each individual order must be less than 200lbs.", 400

  # if ci['quantity'] > 20:
  #   return "Cart item quantity is too large, must be 20 or less", 400
  return db.update_cart_item(current_user.user_id, ci['cart_item_id'], ci['product_id'], ci['quantity'])




# NOTE TO SELF: Test to see what happens if remove cart item id that doesnt exist
@app.route('/removeCartItem', methods=['POST'])
@login_required
def remove_cart_item():
  ci = request.get_json()
  db.delete_cart_item(current_user.user_id, ci['cart_item_id'])
  return 'Success'


# #
# # Order Routes
# #
@app.route('/getOrders', methods=['GET'])
@login_required
def get_orders():
  return db.select_orders(current_user.user_id)


@app.route('/getAllOrders', methods=['GET'])
@admin_required
def get_all_orders():
  return db.select_all_orders()


@app.route('/getOrderItems', methods=['GET'])  # ?orderID=<orderID>
@login_required
def get_order_items():
  # pdb.set_trace()
  order_id = request.args['orderID']
  return db.select_order_items(current_user.user_id, order_id)


@app.route('/getOrderItemsEmployee', methods=["GET"]) # ?orderID=<orderID>
@admin_required
def get_order_items_employee():
  user_id = request.args["userID"]
  order_id = request.args["orderID"]
  return db.select_order_items(user_id=user_id, order_id=order_id)



'''
Place user's order by updating DB product quantities and user order history, then generate new route if there is enough inventory.
  Input:
  * JSON that maps product ID's to order quantities
  Output:
  * If there is enough inventory/quantity for all products in order, returns the order that has been placed 
  * If there is not enough inventory/quantity for all products in order, returns 400 error
  * If the calling user does not have a valid address set, returns 400 error
'''
@app.route('/placeOrder', methods=['POST'])
@login_required
def place_order():
  if current_user.address is None:
    return "No valid address set.", 400

  order_items = request.get_json()
  total_cart_weight = calculate_total_cart_weights(order_items)
  if total_cart_weight > 200.0:
    return "Order is too heavy to purchase. Will not be able to create route.", 400
  if db.purchase_product_order(order_items):
    order = db.insert_order(current_user.user_id, order_items)

    # Start thread to create route if the requirements are met.
    threading.Thread(target=route_if_ready).start()

    return order
  else: 
    return "Not enough items in inventory", 400
  
def update_inventory(order):
  if not bool(order):
    return True
  head_item_num = order.keys()[0]
  head_item_ct = order[head_item_num]
  item_dict = db.select_product(head_item_num)
  old_quantity = item_dict['quantity']
  new_quantity = old_quantity - head_item_ct
  if new_quantity < 0:
    return False
  else:
    db.update_product(head_item_num, item_dict['name'], item_dict['description'], item_dict['image'], new_quantity, item_dict['price'], item_dict['weight'])
    if not update_inventory(order.pop(head_item_ct)):
      db.update_product(head_item_num, item_dict['name'], item_dict['description'], item_dict['image'], old_quantity, item_dict['price'], item_dict['weight'])
      return False
    else:
      return True
    
# #
# # Path Planning Routes
# #
@app.route('/getRoutesList', methods=['GET'])
@admin_required
def get_routes_list():
  return db.select_all_routeid()


@app.route('/getRoute', methods=['GET'])  # ?order_id=<order_id> | ?route_id=<route_id>
@admin_required
def get_route():
  print("debug in get route")
  print("is admin: ", current_user.is_admin)
  if 'route_id' in request.args:
    print("DEBUG: ", request.args["route_id"])
    return db.select_route_from_routeid(request.args['route_id'])

  if 'order_id' in request.args:
    return db.select_route_from_orderid(request.args['order_id'])

  return "Bad Query String", 400


# modifying /getRoute to retunr the user_id with each leg
@app.route('/getRouteWithUsername', methods=['GET'])  # ?route_id=<route_id>
@admin_required
def get_route_with_username():
  print("debug in get route")
  print("is admin: ", current_user.is_admin)
  if 'route_id' in request.args:
    print("DEBUG: ", request.args["route_id"])
    return db.select_route_from_routeid_with_username(request.args['route_id'])

  return "Bad Query String", 400


@app.route('/getMapConstants', methods=['GET'])
@admin_required
def get_map_constants():
  return {"API_KEY": API_KEY, "robot_origin": ORIGIN}


@app.route('/getPlacesConstants', methods=['GET'])
@login_required
def get_places_constants():
    return {"API_KEY": PLACES_API_KEY}


if __name__ == '__main__':
  app.run()
