import db
from groute import grouteInputOrder, grouteResponse, plan_path
import json
import threading
from flask import Flask, request, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
login_manager = LoginManager()
app = Flask(__name__)
app.secret_key = b'replace_this_later'  # TODO: use enviroment variable instead

login_manager.init_app(app)
login_manager.login_view = "login"


class User:
  def __init__(self, user_id, username, password, address):
    self.user_id = user_id
    self.username = username
    self.password = password
    self.address = address
    self.is_active = True

  def get_id(self):
    return str(self.user_id)

  def is_authenticated(self):
    return True

  def is_active(self):
    return self.is_active

  def is_anonymous(self):
    return False

  @staticmethod
  def get(user_id):
    try:
      u = db.select_user(user_id)
      return User(user_id, u['username'], u['password'], u['address'])
    except:
      return None


@login_manager.user_loader
def load_user(user_id):
  return User.get(user_id)


def route_if_ready():
  print("started route if ready thread")
  batch = db.get_path_planning_batch()
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
@app.route('/')
def root():
  return send_from_directory('ogo/dist', 'index.html')


@app.route('/<path:path>')
def assets(path):
  return send_from_directory('ogo/dist', path)


# #
# # User Authentication Routes
# #
@app.route('/signup', methods=['POST'])
def signup():
  u = request.get_json()

  # If the user already exists log them in.
  j = db.validate_user(u['username'], u['password'])
  if j:
    login_user(load_user(j['user_id']))
    return 'Login Success'
  
  user_char_ct = len(u['username'])
  pass_char_ct = len(u['password'])
  if user_char_ct > 20 or user_char_ct < 1:
    return 'Invalid username character count', 400
  if pass_char_ct > 20 or pass_char_ct < 1:
    return 'Invalid password character count', 400
  
  u = db.insert_user(u['username'], u['password'], u['address'])
  login_user(load_user(u['user_id']))  # Log the user in after they add their account to the db
  return 'Signup Success'
  # TODO: handle errors such as no key.


@app.route('/login', methods=['POST'])
def login():
  u = request.get_json()
  j = db.validate_user(u['username'], u['password'])
  if j:
    login_user(load_user(j['user_id']))
    return 'Success'
  return 'Failure'


@app.route('/logout')
@login_required

def logout():
  msg = f"Logging out {current_user.username}"
  logout_user()
  return msg


@app.route('/updateUser', methods=['POST'])
@login_required
def update_user():
  u = request.get_json()
  user_char_ct = len(u['username'])
  pass_char_ct = len(u['password'])
  
  if user_char_ct > 20 or user_char_ct < 1:
    return 'Invalid username character count', 400
  if pass_char_ct > 20 or pass_char_ct < 1:
    return 'Invalid password character count', 400
  
  user_entry = db.validate_user(u['username'], u['password'])
  if user_entry == None or (user_entry['username'] == current_user.username and user_entry['password'] == current_user.password):   # User needs to check to see if the user's username/password matches anyone else OTHER than the one currently logged in
    return db.update_user(current_user.user_id, u['username'], u['password'], u['address'])
  else:
    return "Invalid Entry - User Already Exists"


@app.route('/getUser', methods=['GET'])
@login_required
def get_user():
  return {'user_id': current_user.user_id, 'username': current_user.username, 'address': current_user.address}


# #
# # Product Routes
# #
@app.route('/getProducts', methods=['GET'])
def get_products():
  return json.dumps(db.select_products())


@app.route('/getProduct', methods=['GET'])  # ?productID=<product_id>
def get_product():
  product_id = request.args['productID']
  # TODO: handle if productID is not present in query string
  return json.dumps(db.select_product(product_id))


@app.route('/updateProduct', methods=['POST'])
def update_product():
  p = request.get_json()
  return db.update_product(p['product_id'], p['name'], p['description'], p['image'], p['quantity'], p['price'], p['weight'])


@app.route('/createProduct', methods=['POST'])
def create_product():
  p = request.get_json()
  return db.insert_product(p['name'], p['description'], p['image'], p['quantity'], p['price'], p['weight'])


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
  return db.insert_cart_item(current_user.user_id, ci['product_id'], ci['quantity'])


@app.route('/updateCartItem', methods=['POST'])
@login_required
def update_cart_item():
  ci = request.get_json()
  return db.update_cart_item(current_user.user_id, ci['cart_item_id'], ci['product_id'], ci['quantity'])


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


@app.route('/getOrderItems', methods=['GET'])  # ?orderID=<orderID>
@login_required
def get_order_items():
  order_id = request.args['orderID']
  return db.select_order_items(current_user.user_id, order_id)


@app.route('/placeOrder', methods=['POST'])
@login_required
def place_order():
  order_items = request.get_json()
  if update_inventory(order_items):
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
@login_required  # TODO: Eventually make this admin user only
def get_routes_list():
  return db.select_all_routeid()


@app.route('/getRoute', methods=['GET'])  # ?order_id=<order_id> | ?route_id=<route_id>
@login_required  # TODO: Eventually make this admin user only
def get_route():
  if 'route_id' in request.args:
    return db.select_route_from_routeid(request.args['route_id'])

  if 'order_id' in request.args:
    return db.select_route_from_orderid(request.args['order_id'])

  return "Bad Query String", 400


if __name__ == '__main__':
  app.run()
