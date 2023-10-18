import sqlite3
import time

con = sqlite3.connect("db.db", check_same_thread=False)
cur = con.cursor()


def init():
  cur.executescript('''
  CREATE TABLE IF NOT EXISTS USERS (
      UserID INTEGER PRIMARY KEY,
      Username TEXT,
      Password TEXT,
      Address TEXT,
      IsAdmin INTEGER
  );

  CREATE TABLE IF NOT EXISTS PRODUCTS (
      ProductID INTEGER PRIMARY KEY,
      Name TEXT,
      Description TEXT,
      Image TEXT,
      Quantity INTEGER,
      Price REAL,
      Weight REAL
  );

  CREATE TABLE IF NOT EXISTS CARTS (
      CartID INTEGER PRIMARY KEY,
      UserID INTEGER REFERENCES USERS(UserID)
  );

  CREATE TABLE IF NOT EXISTS CART_ITEMS (
      CartItemID INTEGER PRIMARY KEY,
      CartID INTEGER REFERENCES CARTS(CartID),
      ProductID INTEGER REFERENCES PRODUCTS(ProductID),
      Quantity INTEGER
  );

  CREATE TABLE IF NOT EXISTS ORDERS (
      OrderID INTEGER PRIMARY KEY,
      UserID INTEGER REFERENCES USERS(UserID),
      TotalPrice REAL,
      TotalWeight REAL,
      Status INTEGER,
      PlacedEpoch INTEGER,
      ETAEpoch INTEGER
  );

  CREATE TABLE IF NOT EXISTS ORDER_ITEMS (
      OrderItemID INTEGER PRIMARY KEY,
      OrderID INTEGER REFERENCES ORDERS(OrderID),
      ProductID INTEGER REFERENCES PRODUCTS(ProductID),
      Quantity INTEGER
  );

  CREATE TABLE IF NOT EXISTS ROUTES (
      RouteID INTEGER PRIMARY KEY,
      Polyline TEXT,
      CreationEpoch INTEGER
  );

  CREATE TABLE IF NOT EXISTS ROUTE_ORDERS (
      RouteOrderID INTEGER PRIMARY KEY,
      RouteID INTEGER REFERENCES ROUTES(RouteID),
      OrderID INTEGER REFERENCES ORDERS(OrderID),
      Sequence INTEGER,
      Lat REAL,
      Lon REAL
  );
''')
  # TODO: Add more contraints (such as NOT NULL) to above tables.
  con.commit()


# #
# # Products
# #


def insert_product(name: str, description: str, image: str, quantity: int, price: float, weight: float) -> dict:
  cur.execute("INSERT INTO PRODUCTS (Name, Description, Image, Quantity, Price, Weight) VALUES (?, ?, ?, ?, ?, ?)",
              (name, description, image, quantity, price, weight))
  con.commit()

  product_id = cur.lastrowid
  return {'product_id': product_id, 'name': name, 'description': description, 'image': image, 'quantity': quantity, 'price': price, 'weight': weight}


def update_product(product_id: int, name: str, description: str, image: str, quantity: int, price: float, weight: float) -> dict:
  cur.execute("UPDATE PRODUCTS SET Name=?, Description=?, Image=?, Quantity=?, Price=?, Weight=? WHERE ProductID=?",
              (name, description, image, quantity, price, weight, product_id))
  con.commit()
  return {'product_id': product_id, 'name': name, 'description': description, 'image': image, 'quantity': quantity, 'price': price, 'weight': weight}
  # TODO: possibly return false or throw error if there is not a product in the db with the given productid


def select_product(product_id: int) -> dict:
  cur.execute("SELECT * FROM PRODUCTS WHERE ProductID=?", (product_id,))
  row = cur.fetchone()
  return {'product_id': row[0], 'name': row[1], 'description': row[2], 'image': row[3], 'quantity': row[4], 'price': row[5], 'weight': row[6]}


def select_products() -> list[dict]:
  cur.execute("SELECT * FROM PRODUCTS")
  return [{'product_id': row[0], 'name': row[1], 'description': row[2], 'image': row[3], 'quantity': row[4], 'price': row[5], 'weight': row[6]} for row in cur.fetchall()]


# #
# # Users
# #

def select_user(user_id) -> dict:
  cur.execute("SELECT * FROM USERS WHERE UserID=?", (user_id,))
  row = cur.fetchone()
  return {'user_id': row[0], 'username': row[1], 'password': row[2], 'address': row[3], 'is_admin': bool(row[4])}


def validate_user(username, password) -> dict:
  cur.execute("SELECT * FROM USERS WHERE Username=? AND Password=?", (username, password))
  row = cur.fetchone()
  if row == None:
    return None
  return {'user_id': row[0], 'username': row[1], 'password': row[2], 'address': row[3], 'is_admin': bool(row[4])}


def insert_user(username: str, password: str, address: str, is_admin: bool) -> dict:
  cur.execute("INSERT INTO USERS (Username, Password, Address, IsAdmin) VALUES (?, ?, ?, ?)",
              (username, password, address, int(is_admin)))
  con.commit()

  user_id = cur.lastrowid
  return {'user_id': user_id, 'username': username, 'password': password, 'address': address, 'is_admin': is_admin}


def update_user(user_id: int, username: str, password: str, address: str, is_admin: bool) -> None:
  cur.execute("UPDATE USERS SET Username=?, Password=?, Address=?, IsAdmin=? WHERE UserID=?",
              (username, password, address, int(is_admin), user_id))
  con.commit()
  return {'user_id': user_id, 'username': username, 'password': password, 'address': address, 'is_admin': is_admin}


# #
# # Carts
# #


def get_cart_id(user_id: int) -> int:
  cur.execute("SELECT CartID FROM CARTS WHERE UserID=?", (user_id,))
  cart_row = cur.fetchone()

  # If the cart does not exist yet. Create it and then return the cart_id.
  if cart_row == None:
    return insert_cart(user_id)['cart_id']

  return cart_row[0]


def select_cart(user_id: int) -> dict:
  cart_id = get_cart_id(user_id)

  cur.execute("SELECT P.ProductID, P.Name, P.Description, P.Image, P.Price, P.Weight, CI.CartItemID, CI.Quantity "
              "FROM CART_ITEMS AS CI "
              "JOIN PRODUCTS AS P ON CI.ProductID = P.ProductID "
              "WHERE CI.CartID=?", (cart_id,))

  return {
    "cart_id": cart_id,
    "items": [{"cart_item_id": ci[6], "quantity": ci[7], "product_id": ci[0], "name": ci[1], "description": ci[2], "image":ci[3], "price": ci[4], "weight": ci[5]} for ci in cur.fetchall()]
  }


def insert_cart(user_id: int) -> dict:
  cur.execute("INSERT INTO CARTS (UserID) VALUES (?)", (user_id,))
  con.commit()
  cart_id = cur.lastrowid
  return {"cart_id": cart_id, "user_id": user_id}


def insert_cart_item(user_id: int, product_id: int, quantity: int) -> dict:
  cart_id = get_cart_id(user_id)

  cur.execute("INSERT INTO CART_ITEMS (CartID, ProductID, Quantity) VALUES (?, ?, ?)",
              (cart_id, product_id, quantity))
  con.commit()

  cart_item_id = cur.lastrowid
  return {"cart_item_id": cart_item_id, "product_id": product_id, "quantity": quantity}


def update_cart_item(user_id: int, cart_item_id: int, product_id: int, quantity: int) -> dict:
  cart_id = get_cart_id(user_id)

  cur.execute("UPDATE CART_ITEMS SET Quantity=?, ProductID=? WHERE CartItemID=? AND CartID=?", (quantity, product_id, cart_item_id, cart_id))
  con.commit()

  return {"cart_item_id": cart_item_id, "product_id": product_id, "quantity": quantity}


def delete_cart_item(user_id: int, cart_item_id: int) -> None:
  cart_id = get_cart_id(user_id)

  cur.execute("DELETE FROM CART_ITEMS WHERE CartItemID=? AND CartID=?", (cart_item_id, cart_id))
  con.commit()


# #
# # Orders
# #


def select_orders(user_id: int) -> list[dict]:
  cur.execute("SELECT * FROM ORDERS WHERE UserID=?", (user_id,))

  return [{
    'order_id': o[0],
    'user_id': o[1],
    'total_price': o[2],
    'total_weight': o[3],
    'status': o[4],
    'placed_epoch': o[5],
    'eta_epoch': o[6]
  } for o in cur.fetchall()]


def select_order_items(user_id: int, order_id: int) -> list[dict]:
  # TODO: ensure that the user owns the order

  cur.execute("SELECT P.ProductID, P.Name, P.Description, P.Image, P.Price, P.Weight, OI.OrderItemID, OI.Quantity "
              "FROM ORDER_ITEMS AS OI "
              "JOIN PRODUCTS AS P ON OI.ProductID = P.ProductID "
              "WHERE OI.OrderID=?", (order_id,))

  return [{
    'product_id': o[0],
    'name': o[1],
    'description': o[2],
    'image': o[3],
    'price': o[4],
    'weight': o[5],
    'order_item_id': o[6],
    'quantity': o[7]
  } for o in cur.fetchall()]


def calc_total_price_weight(order_items):
  total_price = 0
  total_weight = 0

  for o in order_items:
    p = select_product(o['product_id'])
    total_price += p['price'] * o['quantity']
    total_weight += p['weight'] * o['quantity']

  return total_price, total_weight


# order_items = [
#   {
#     'product_id': 1,
#     'quantity': 2
#   },
#   {
#     'product_id': 1,
#     'quantity': 2
#    }
# ]
def insert_order(user_id: int, order_items: list[dict]) -> dict:
  total_price, total_weight = calc_total_price_weight(order_items)
  status = 0
  placed_epoch = int(time.time())

  cur.execute("INSERT INTO ORDERS (UserID, TotalPrice, TotalWeight, Status, PlacedEpoch) VALUES (?, ?, ?, ?, ?)",
              (user_id, total_price, total_weight, status, placed_epoch))

  order_id = cur.lastrowid
  for o in order_items:
    cur.execute("INSERT INTO ORDER_ITEMS (OrderID, ProductID, Quantity) VALUES (?, ?, ?)",
                (order_id, o['product_id'], o['quantity']))

  con.commit()

  return {'order_id': order_id, 'total_price': total_price, 'total_weight': total_weight, 'status': status, 'placed_epoch': placed_epoch}


# #
# # Routes
# #


# legs = [
#   {
#     'order_id': 1,
#     'sequence': 0,
#     'lat': -120.2343,
#     'lon': 73.4554,
#     'eta': 1696845362
#   }
# ]
def insert_route(polyline: str, legs: list[dict]):
  cur.execute("INSERT INTO ROUTES (Polyline, CreationEpoch) VALUES (?, ?)",
              (polyline, int(time.time())))

  route_id = cur.lastrowid

  for l in legs:
    cur.execute("INSERT INTO ROUTE_ORDERS (RouteID, OrderID, Sequence, Lat, Lon) VALUES (?, ?, ?, ?, ?)",
                (route_id, l['order_id'], l['sequence'], l['lat'], l['lon']))

    cur.execute("UPDATE ORDERS SET ETAEpoch=?, Status=? WHERE OrderID=?",
                (l['eta'] + int(time.time()), 1, l['order_id']))

  con.commit()


def select_all_routeid() -> list[int]:
  cur.execute("SELECT * FROM ROUTES")
  return [{"route_id": r[0], "creation_epoch": r[2]} for r in cur.fetchall()]


def select_route_from_routeid(route_id: int):
  cur.execute("SELECT * FROM ROUTES WHERE RouteID=?", (route_id,))
  r = cur.fetchone()
  polyline = r[1]
  creation_epcoh = r[2]

  cur.execute("SELECT * FROM ROUTE_ORDERS WHERE RouteID=?", (route_id,))
  legs = [{
    'order_id': l[2],
    'sequence': l[3],
    'lat': l[4],
    'lon': l[5]
  } for l in cur.fetchall()]

  return {
    'route_id': route_id,
    'polyline': polyline,
    'creation_epcoh': creation_epcoh,
    'legs': legs
  }


def select_route_from_orderid(order_id: int):
  cur.execute("SELECT RouteID FROM ROUTE_ORDERS WHERE OrderID=?", (order_id,))
  return select_route_from_routeid(cur.fetchone()[0])


def get_path_planning_batch():
  cur.execute("SELECT O.OrderID, O.TotalWeight, U.Address "
              "FROM ORDERS AS O "
              "JOIN USERS AS U ON U.UserID = O.UserID "
              "WHERE O.Status=?", (0,))

  batch = []
  total_weight = 0.0
    
  for row in cur.fetchall():
    order_id, weight, address = row

    if total_weight + weight <= 200.0 and len(batch) < 10:
      batch.append({"order_id": order_id, "address": address})
      total_weight += weight
    else:
      total_weight += weight
      return batch

  if len(batch) == 10 or total_weight >= 200.0:
    return batch
  else:
    return None



init()
