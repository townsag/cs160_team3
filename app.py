import db
import json
import configparser
import os

import requests
from flask import Flask, request, send_from_directory, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

login_manager = LoginManager()
app = Flask(__name__)
app.secret_key = b'replace_this_later' 
config = configparser.ConfigParser()
config.read('.env')
api_key = config['KEYS']['GOOGLE_ROUTES_API_KEY']
origin = "1 Washington Sq, San Jose, CA 95192"
base_url = "https://maps.googleapis.com/maps/api/directions/json"


login_manager.init_app(app)


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
  if db.validate_user(u['username'], u['password']):
    login_user(load_user(j['user_id']))
    return 'Success'

  u = db.insert_user(u['username'], u['password'], u['address'])
  login_user(load_user(u['user_id']))  # Log the user in after they add their account to the db
  return 'Success'
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
  return db.update_user(current_user.user_id, u['username'], u['password'], u['address'])


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
  return db.insert_order(current_user.user_id, order_items)

@app.route('/getDistance', methods=['GET'])
def get_distance():
  destination = request.args.get('destination') 
  response = google_api_request(destination)
  print(response.text)
  if response.status_code == 200:
    data = response.json()
    if "routes" in data and len(data["routes"]) > 0:
        travel_distance = data["routes"][0]["distanceMeters"]
        return jsonify({'travelDistance' : travel_distance})
    else:
        print( len(data["routes"]))
        return jsonify({"error": "No route found."})
  else:
    print(response.status_code)
    return jsonify({"error": "Error in the API request."})


@app.route('/getTime', methods=['GET'])
def get_time():
  destination = request.args.get('destination') 
  response = google_api_request(destination)
  print(response.text)
  if response.status_code == 200:
    data = response.json()
    if "routes" in data and len(data["routes"]) > 0:
        travel_time = data["routes"][0]["duration"]
        return jsonify({'travelTime' : travel_time})
    else:
        print( len(data["routes"]))
        return jsonify({"error": "No route found."})
  else:
    print(response.status_code)
    return jsonify({"error": "Error in the API request."})

@app.route('/getPolyLine', methods=['GET'])
def get_poly_line():
  destination = request.args.get('destination') 
  response = google_api_request(destination)
  print(response.text)
  if response.status_code == 200:
    data = response.json()
    if "routes" in data and len(data["routes"]) > 0:
        poly_line = data["routes"][0]["polyline"]['encodedPolyline']
        return jsonify({'polyLine' : poly_line})
    else:
        print( len(data["routes"]))
        return jsonify({"error": "No route found."})
  else:
    print(response.status_code)
    return jsonify({"error": "Error in the API request."})

def google_api_request(destination):
  headers = {
    'Content-Type': 'application/json',
    'X-Goog-Api-Key': api_key,
    'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline',
  }
  json_data = {
      'origin': {
          'address': origin
      },
      'destination': {
          'address': destination
      },
      'travelMode': 'DRIVE',
      'routingPreference': 'TRAFFIC_AWARE',
      'departureTime': '2023-10-15T15:01:23.045123456Z',
      'computeAlternativeRoutes': False,
      'routeModifiers': {
          'avoidTolls': False,
          'avoidHighways': False,
          'avoidFerries': False,
      },
      'languageCode': 'en-US',
      'units': 'IMPERIAL',
  }
  return requests.post('https://routes.googleapis.com/directions/v2:computeRoutes', headers=headers, json=json_data)

if __name__ == '__main__':
  app.run()
