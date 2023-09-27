import db
import json
from flask import Flask, request

app = Flask(__name__)


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


@app.route('/cart', methods=['GET'])
def get_cart():
  pass


@app.route('/cart', methods=['POST'])
def post_cart():
  pass


@app.route('/orders', methods=['GET'])
def get_orders():
  pass


@app.route('/orderItems', methods=['GET'])
def get_order_items():
  pass


if __name__ == '__main__':
  app.run()
