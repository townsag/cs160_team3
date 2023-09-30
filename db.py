import sqlite3
con = sqlite3.connect("db.db", check_same_thread=False)
cur = con.cursor()


def init():
  cur.executescript('''
  CREATE TABLE IF NOT EXISTS USERS (
      UserID INTEGER PRIMARY KEY,
      Username TEXT,
      Password TEXT,
      Address TEXT
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
      Status TEXT,
      Epoch INTEGER
  );

  CREATE TABLE IF NOT EXISTS ORDER_ITEMS (
      OrderItemID INTEGER PRIMARY KEY,
      OrderID INTEGER REFERENCES ORDERS(OrderID),
      ProductID INTEGER REFERENCES PRODUCTS(ProductID),
      Quantity INTEGER
  );

  CREATE TABLE IF NOT EXISTS ROUTES (
      RouteID INTEGER PRIMARY KEY,
      RouteData TEXT
  );

  CREATE TABLE IF NOT EXISTS ROUTE_ORDERS (
      RouteOrderID INTEGER PRIMARY KEY,
      RouteID INTEGER REFERENCES ROUTES(RouteID),
      OrderID INTEGER REFERENCES ORDERS(OrderID)
  );
''')
  # TODO: Add more contraints (such as NOT NULL) to above tables.
  # TODO: Should add flag to USERS table to specify admin user.
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
  return {'user_id': row[0], 'username': row[1], 'password': row[2], 'address': row[3]}


def validate_user(username, password) -> dict:
  cur.execute("SELECT * FROM USERS WHERE Username=? AND Password=?", (username, password))
  row = cur.fetchone()
  if row == None:
    return None
  return {'user_id': row[0], 'username': row[1], 'password': row[2], 'address': row[3]}


def insert_user(username: str, password: str, address: str) -> dict:
  cur.execute("INSERT INTO USERS (Username, Password, Address) VALUES (?, ?, ?)",
              (username, password, address))
  con.commit()

  user_id = cur.lastrowid
  return {'user_id': user_id, 'username': username, 'password': password, 'address': address}


def update_user(user_id: int, username: str, password: str, address: str) -> None:
  cur.execute("UPDATE USERS SET Username=?, Password=?, Address=? WHERE UserID=?",
              (username, password, address, user_id))
  con.commit()
  return {'user_id': user_id, 'username': username, 'password': password, 'address': address}


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


init()
