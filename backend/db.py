import sqlite3
import time
import bcrypt

con = sqlite3.connect("db.db", check_same_thread=False)
cur = con.cursor()

def init():
  cur.executescript('''
  CREATE TABLE IF NOT EXISTS USERS (
      UserID INTEGER PRIMARY KEY,
      Username TEXT,
      Password BLOB,
      Address TEXT,
      IsAdmin INTEGER
  );

  CREATE TABLE IF NOT EXISTS CATEGORIES (
      CategoryID INTEGER PRIMARY KEY,
      Name TEXT
  );             

  CREATE TABLE IF NOT EXISTS PRODUCTS (
      ProductID INTEGER PRIMARY KEY,
      Name TEXT,
      Description TEXT,
      Image TEXT,
      Quantity INTEGER,
      Price REAL,
      Weight REAL,
      CategoryID INTEGER REFERENCES CATEGORIES(CategoryID)
  );

  CREATE TABLE IF NOT EXISTS TAGS (
      TagID INTEGER PRIMARY KEY,
      Name TEXT
  );
                    
  CREATE TABLE IF NOT EXISTS PRODUCT_TAGS (
      ProductTagID INTEGER PRIMARY KEY,
      TagID INTEGER REFERENCES TAGS(TagID),
      ProductID INTEGER REFERENCES PRODUCTS(ProductID)              
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


def insert_product(name: str, description: str, image: str, quantity: int, price: float, weight: float, category_id: int, tags: list[int]) -> dict:
  cur.execute("INSERT INTO PRODUCTS (Name, Description, Image, Quantity, Price, Weight, CategoryID) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (name, description, image, quantity, price, weight, category_id))
  product_id = cur.lastrowid

  for tag_id in tags:
    cur.execute("INSERT INTO PRODUCT_TAGS (TagID, ProductID) VALUES (?, ?)",
                (tag_id, product_id))

  con.commit()

  return select_product(product_id)


def update_product(product_id: int, name: str, description: str, image: str, quantity: int, price: float, weight: float, category_id: int, tags: list[int]) -> dict:
  cur.execute("UPDATE PRODUCTS SET Name=?, Description=?, Image=?, Quantity=?, Price=?, Weight=?, CategoryID=? WHERE ProductID=?",
              (name, description, image, quantity, price, weight, category_id, product_id))

  cur.execute("DELETE FROM PRODUCT_TAGS WHERE ProductID=?", (product_id,))

  for tag_id in tags:
    cur.execute("INSERT INTO PRODUCT_TAGS (TagID, ProductID) VALUES (?, ?)",
                (tag_id, product_id))

  con.commit()

  tags = select_product_tags(product_id)
  return {'product_id': product_id, 'name': name, 'description': description, 'image': image, 'quantity': quantity, 'price': price, 'weight': weight, 'category': select_category(category_id), 'tags': tags}
  # TODO: possibly return false or throw error if there is not a product in the db with the given productid


def select_product(product_id: int) -> dict:
  cur.execute("SELECT * FROM PRODUCTS WHERE ProductID=?", (product_id,))
  prod = cur.fetchone()

  tags = select_product_tags(product_id)

  return {'product_id': prod[0], 'name': prod[1], 'description': prod[2], 'image': prod[3], 'quantity': prod[4], 'price': prod[5], 'weight': prod[6], 'category': select_category(prod[7]), 'tags': tags}


def select_products() -> list[dict]:
  cur.execute("SELECT * FROM PRODUCTS")
  return [{'product_id': row[0], 'name': row[1], 'description': row[2], 'image': row[3], 'quantity': row[4], 'price': row[5], 'weight': row[6], 'category': select_category(row[7]), 'tags': select_product_tags(row[0])} for row in cur.fetchall()]


def search_products(query: str) -> list[dict]:
  cur.execute("SELECT * FROM PRODUCTS WHERE Name LIKE ? COLLATE NOCASE OR Description LIKE ? COLLATE NOCASE", ('%' + query + '%', '%' + query + '%'))
  return [{'product_id': row[0], 'name': row[1], 'description': row[2], 'image': row[3], 'quantity': row[4], 'price': row[5], 'weight': row[6], 'category': select_category(row[7]), 'tags': select_product_tags(row[0])} for row in cur.fetchall()]


def insert_tag(name: str) -> dict:
  cur.execute("INSERT INTO TAGS (Name) VALUES (?)",
              (name,))
  con.commit()

  tag_id = cur.lastrowid
  return {'tag_id': tag_id, 'name': name}


def select_all_tags() -> list[dict]:
  cur.execute("SELECT * FROM TAGS")
  return [{'tag_id': t[0], 'name': t[1]} for t in cur.fetchall()]


def select_product_tags(product_id:int) -> list[dict]:
  cur.execute("SELECT T.TagID, T.Name "
              "FROM PRODUCT_TAGS AS PT "
              "JOIN Tags AS T ON T.TagID = PT.TagID "
              "WHERE PT.ProductID=?", (product_id,))
  return [{'tag_id': t[0], 'name': t[1]} for t in cur.fetchall()]


def update_tag(tag_id: int, name: str) -> dict:
  cur.execute("UPDATE TAGS SET Name=? WHERE TagID=?",
              (name, tag_id))
  con.commit()

  return {'tag_id': tag_id, 'name': name}


def select_all_categories() -> list[dict]:
  cur.execute("SELECT * FROM CATEGORIES")
  return [{'category_id': c[0], 'name': c[1]} for c in cur.fetchall()]


def select_category(category_id) -> list[dict]:
  cur.execute("SELECT * FROM CATEGORIES WHERE CategoryID=?",
              (category_id,))
  c = cur.fetchone()
  return {'category_id': c[0], 'name': c[1]}


def insert_category(name: str) -> dict:
  cur.execute("INSERT INTO CATEGORIES (Name) VALUES (?)",
              (name,))
  con.commit()

  category_id = cur.lastrowid
  return {'category_id': category_id, 'name': name}


def update_category(category_id: int, name: str) -> dict:
  cur.execute("UPDATE CATEGORIES SET Name=? WHERE CategoryID=?",
              (name, category_id))
  con.commit()

  return {'category_id': category_id, 'name': name}



# #
# # Users
# #

def select_user(user_id: int) -> dict:
  cur.execute("SELECT * FROM USERS WHERE UserID=?", (user_id,))
  row = cur.fetchone()
  return {'user_id': row[0], 'username': row[1], 'address': row[3], 'is_admin': bool(row[4])}


def validate_user(username: str, password: str) -> dict:
  cur.execute("SELECT * FROM USERS WHERE Username=?", (username,))
  row = cur.fetchone()
  
  if row != None and bcrypt.checkpw(password.encode('utf-8'), row[2]):
    return {'user_id': row[0], 'username': row[1], 'address': row[3], 'is_admin': bool(row[4])}
  
  return None


def insert_user(username: str, password: str, address: str, is_admin: bool) -> dict:
  hashedpw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

  cur.execute("INSERT INTO USERS (Username, Password, Address, IsAdmin) VALUES (?, ?, ?, ?)",
              (username, hashedpw, address, int(is_admin)))
  con.commit()

  user_id = cur.lastrowid
  return {'user_id': user_id, 'username': username, 'address': address, 'is_admin': is_admin}


def update_user_username(user_id: int, username: str):
  cur.execute("UPDATE USERS SET Username=? WHERE UserID=?",
              (username, user_id))
  con.commit()


def update_user_password(user_id: int, password: str) -> None:
  hashedpw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  cur.execute("UPDATE USERS SET Password=? WHERE UserID=?",
              (hashedpw, user_id))
  con.commit()


def update_user_address(user_id: int, address: str) -> None:
  cur.execute("UPDATE USERS SET Address=? WHERE UserID=?",
              (address, user_id))
  con.commit()


def update_user_admin(user_id: int, is_admin: bool) -> None:
  cur.execute("UPDATE USERS SET IsAdmin=? WHERE UserID=?",
              (int(is_admin), user_id))
  con.commit()

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
