# ==========BEFORE RUNNING THIS SCIPT==========#
#   - start the flask server


import requests
session = requests.Session()

import db
db.delete_all_tables()

base_url = "http://127.0.0.1:5000"

admin_1 = {'username': 'Andrew1', 'password': 'asdfqwer', 
           'address': '1148 La Terrace Cir. San Jose, CA 95123', "is_admin":1}
user_2 = {'username': 'Sabrina1', 'password': 'asdfqwer', 
           'address': '461 Blossom Hill rd. San Jose, CA 95123', "is_admin":0}
user_3 = {'username': 'Dustin1', 'password': 'asdfqwer', 
           'address': '19501 Stevens Creek Blvd. Cupertino, CA 95014', "is_admin":0}
user_4 = {'username': 'Klyde1', 'password': 'asdfqwer', 
           'address': '2056 Fairway Glen Dr. Santa Clara, CA 95054', "is_admin":0}


# add a new admin user to the database
request1 = session.post(url="http://127.0.0.1:5000/signup", json=admin_1)
request1 = session.post(url="http://127.0.0.1:5000/updateUser", json={"address": '1148 La Terrace Cir. San Jose, CA 95123', "is_admin": True})
request1 = session.get(url="http://127.0.0.1:5000/getUser")
print(request1.text)
request1 = session.get(url="http://127.0.0.1:5000/logout")


# add the rest of the admin users
for user_data in [user_2, user_3, user_4]:
    request2 = session.post(url="http://127.0.0.1:5000/signup", json=user_data)
    print(request2.text)
    temp = {}
    temp["address"] = user_data["address"]
    request2 = session.post(url="http://127.0.0.1:5000/updateUser", json=temp)
    request2 = session.get(url="http://127.0.0.1:5000/getUser")
    print(request2.text, "\n")
    request2 = session.get(url="http://127.0.0.1:5000/logout")


# create product categories
request3 = session.post(url="http://127.0.0.1:5000/login", json={"username":"Andrew1", "password": "asdfqwer"})
request3 = session.post(url="http://127.0.0.1:5000/createCategory", json={"name":"Fruits"})
request3 = session.post(url="http://127.0.0.1:5000/createCategory", json={"name":"Protein"})
request3 = session.post(url="http://127.0.0.1:5000/createCategory", json={"name":"Nuts"})
request3 = session.post(url="http://127.0.0.1:5000/createCategory", json={"name":"Vegetable"})
request3 = session.get(url="http://127.0.0.1:5000/getCategories")
print(request3.text)


# create product tags
request3 = session.post(url="http://127.0.0.1:5000/createTag", json={"name":"Gluten Free"})
request3 = session.post(url="http://127.0.0.1:5000/createTag", json={"name":"Vegetarian"})
request3 = session.post(url="http://127.0.0.1:5000/createTag", json={"name":"Vegan"})
request3 = session.post(url="http://127.0.0.1:5000/createTag", json={"name":"Lactose Free"})
request3 = session.post(url="http://127.0.0.1:5000/createTag", json={"name":"Nut Free"})
request3 = session.get(url="http://127.0.0.1:5000/getTags")
print(request3.text)

# populate the database with products
products = [
{'name': 'Apple',
  'description': 'Fresh and crisp apple, rich in vitamins and fiber',
  'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTN2Hgg8YOw4ntI9XZl0XX4ppf2VmSYyMrwJjFJhpYJrMeMt6y0XcMqdrQwUytsYfMldkI&usqp=CAU',
  'quantity': 100,
  'price': 19.99,
  'weight': 5.51,
  'category_id': 1,
  'tags': [1, 2, 3, 4, 5]},
 {'name': 'Almonds',
  'description': 'Premium quality almonds, packed with healthy fats and protein',
  'image': 'https://www.healthysupplies.co.uk/pics/almonds-catpic21.jpg',
  'quantity': 50,
  'price': 23.99,
  'weight': 6.17,
  'category_id': 3,
  'tags': [1, 2, 3, 4]},
 {'name': 'Eggplant',
  'description': 'Organic eggplant, perfect for various culinary delights',
  'image': 'https://mucci-production-user-uploads-bucket.s3.amazonaws.com/images/Product-IMG_MiniEggplant-rev.original.png',
  'quantity': 50,
  'price': 23.99,
  'weight': 6.17,
  'category_id': 4,
  'tags': [1, 2, 3, 4, 5]},
 {'name': 'Banana',
  'description': 'Sweet and nutritious banana, a great source of energy',
  'image': 'https://th-thumbnailer.cdn-si-edu.com/4Nq8HbTKgX6djk07DqHqRsRuFq0=/1000x750/filters:no_upscale()/https://tf-cmsv2-smithsonianmag-media.s3.amazonaws.com/filer/d5/24/d5243019-e0fc-4b3c-8cdb-48e22f38bff2/istock-183380744.jpg',
  'quantity': 50,
  'price': 23.99,
  'weight': 6.17,
  'category_id': 1,
  'tags': [1, 2, 3, 4, 5]},
 {'name': 'Beef',
  'description': 'Premium lean beef, a great source of high-quality protein',
  'image': 'https://images.inc.com/uploaded_files/image/1920x1080/getty_80116649_344560.jpg',
  'quantity': 50,
  'price': 23.99,
  'weight': 6.17,
  'category_id': 2,
  'tags': [1, 4, 5]},
 {'name': 'Cheese',
  'description': 'Aged cheddar cheese, rich in calcium and delicious flavor',
  'image': 'https://cdn.britannica.com/60/217660-050-DBCC409A/cheddar-cheese-wedge.jpg',
  'quantity': 50,
  'price': 23.99,
  'weight': 6.17,
  'category_id': 2,
  'tags': [1, 5]},
 {'name': 'Chicken',
  'description': 'Premium chicken breast, a versatile and healthy protein option',
  'image': 'https://images.eatthismuch.com/img/395_ldementhon_471464da-daad-4a92-8b5d-7e9a6de898a8.png',
  'quantity': 50,
  'price': 23.99,
  'weight': 6.17,
  'category_id': 2,
  'tags': [1, 4, 5]},
 {'name': 'Walnuts',
  'description': 'Fresh and crunchy walnuts, high in omega-3 fatty acids',
  'image': 'https://cdn.britannica.com/69/124169-050-54860BD1/fruit-walnut-tree-husk.jpg',
  'quantity': 50,
  'price': 23.99,
  'weight': 6.17,
  'category_id': 3,
  'tags': [1, 2, 3, 4]},
 {'name': 'Orange',
  'description': 'Sweet and citrusy fruit',
  'image': 'https://www.mz-store.com/blog/wp-content/uploads_en/2020/11/shutterstock_342874121.jpg',
  'quantity': 50,
  'price': 14.99,
  'weight': 3.3,
  'category_id': 1,
  'tags': [1, 2, 3, 4, 5]},
 {'name': 'Salmon',
  'description': 'Healthy and delicious fish',
  'image': 'https://m.media-amazon.com/images/I/511ld5XjFwL.jpg',
  'quantity': 50,
  'price': 29.99,
  'weight': 0.75,
  'category_id': 2,
  'tags': [1, 4, 5]},
 {'name': 'Cashews',
  'description': 'Creamy and crunchy nuts',
  'image': 'https://nuts.com/images/rackcdn/ed910ae2d60f0d25bcb8-80550f96b5feb12604f4f720bfefb46d.ssl.cf1.rackcdn.com/62d4000cb074ab08-0HVMW7Um-zoom.jpg',
  'quantity': 50,
  'price': 19.99,
  'weight': 5.1,
  'category_id': 3,
  'tags': [1, 2, 3, 4]},
 {'name': 'Spinach',
  'description': 'Nutrient-rich leafy green',
  'image': 'https://farmfreshcarolinas.com/wp-content/uploads/2019/02/Baby-spinach-scaled.jpg',
  'quantity': 50,
  'price': 9.99,
  'weight': 0.88,
  'category_id': 4,
  'tags': [1, 2, 3, 4, 5]},
 {'name': 'Peach',
  'description': 'Juicy and flavorful fruit',
  'image': 'https://www.eatrightbasket.com/wp-content/uploads/2019/06/Peach.jpg',
  'quantity': 50,
  'price': 16.99,
  'weight': 3.8,
  'category_id': 1,
  'tags': [1, 2, 3, 4, 5]},
 {'name': 'Tofu',
  'description': 'Versatile plant-based protein',
  'image': 'https://static.vecteezy.com/system/resources/previews/022/841/506/large_2x/white-tofu-and-green-leaves-isolated-on-white-background-with-clipping-path-photo.jpg',
  'quantity': 50,
  'price': 12.99,
  'weight': 2.2,
  'category_id': 2,
  'tags': [1, 2, 3, 4, 5]},
 {'name': 'Pistachios',
  'description': 'Delicious and healthy nuts',
  'image': 'https://candylandstore.com/wp-content/uploads/2016/08/pistachio.jpg',
  'quantity': 50,
  'price': 21.99,
  'weight': 5.7,
  'category_id': 3,
  'tags': [1, 2, 3, 4]},
 {'name': 'Broccoli',
  'description': 'Nutritious cruciferous vegetable',
  'image': 'https://thumbs.dreamstime.com/b/fresh-green-broccoli-white-background-organic-food-151980220.jpg',
  'quantity': 50,
  'price': 8.99,
  'weight': 1.5,
  'category_id': 4,
  'tags': [1, 2, 3, 4, 5]},
 {'name': 'Mango',
  'description': 'Sweet tropical fruit',
  'image': 'https://wallpapers.com/images/hd/mango-background-9no344bpdko4hrrs.jpg',
  'quantity': 50,
  'price': 18.99,
  'weight': 2.8,
  'category_id': 1,
  'tags': [1, 2, 3, 4, 5]},
 {'name': 'Chickpeas',
  'description': 'Protein-packed legumes',
  'image': 'https://t3.ftcdn.net/jpg/02/83/97/16/360_F_283971637_l01oKnCdtSDjeSrr0HzsK35wQtx91CNc.jpg',
  'quantity': 50,
  'price': 7.99,
  'weight': 2.0,
  'category_id': 4,
  'tags': [1, 2, 3, 4, 5]}]

for product in products:
    request4 = session.post(url="http://127.0.0.1:5000/createProduct", json=product)
    print(request4.text)
request4 = session.get(url="http://127.0.0.1:5000/logout")
print(request4.text)


# populate the carts of the users
users_credentials = [
    {"username":"Dustin1", "password":"asdfqwer"},
    {"username":"Klyde1", "password":"asdfqwer"},
    {'username': 'Sabrina1', 'password': 'asdfqwer'}
]

for user in users_credentials:
    request5 = session.post(url="http://127.0.0.1:5000/login", json=user)
    request5 = session.post(url="http://127.0.0.1:5000/addCartItem", json={"product_id":1, "quantity":3})
    request5 = session.post(url="http://127.0.0.1:5000/addCartItem", json={"product_id":2, "quantity":4})
    request5 = session.post(url="http://127.0.0.1:5000/addCartItem", json={"product_id":3, "quantity":5})
    request5 = session.get(url="http://127.0.0.1:5000/getCart")
    print(request5.text, "\n")
    request5 = session.get(url="http://127.0.0.1:5000/logout")
    

# place the orders of the first two users
for user in users_credentials:
    request6 = session.post(url="http://127.0.0.1:5000/login", json=user)
    cart_list = session.get(url="http://127.0.0.1:5000/getCart").json()["items"]
    request6 = session.post(url="http://127.0.0.1:5000/placeOrder", json=cart_list)
    print(request6.text, "\n")
    cart_list = session.get(url="http://127.0.0.1:5000/getCart").json()["items"]
    for cart_item in cart_list:
        request8 = session.post(url="http://127.0.0.1:5000/removeCartItem", json={"cart_item_id": cart_item["cart_item_id"]})
    request6 = session.get(url="http://127.0.0.1:5000/logout")
    import time
    time.sleep(1.5)


for user in users_credentials:
    request7 = session.post(url="http://127.0.0.1:5000/login", json=user)
    request7 = session.post(url="http://127.0.0.1:5000/addCartItem", json={"product_id":4, "quantity":2})
    request7 = session.post(url="http://127.0.0.1:5000/addCartItem", json={"product_id":7, "quantity":3})
    request7 = session.post(url="http://127.0.0.1:5000/addCartItem", json={"product_id":5, "quantity":4})
    cart_list = session.get(url="http://127.0.0.1:5000/getCart").json()["items"]
    request7 = session.post(url="http://127.0.0.1:5000/placeOrder", json=cart_list)
    for cart_item in cart_list:
        request8 = session.post(url="http://127.0.0.1:5000/removeCartItem", json={"cart_item_id": cart_item["cart_item_id"]})
    request7 = session.get(url="http://127.0.0.1:5000/logout")
    time.sleep(1.5)



# # place one more order so that each user doesnt have the same cart, this makes debugging easier
# request8 = session.post(url="http://127.0.0.1:5000/login", json={"username":"Andrew1", "password":"asdfqwer"})

# request8 = session.post(url="http://127.0.0.1:5000/addCartItem", json={"product_id":4, "quantity":2})
# cart_list = session.get(url="http://127.0.0.1:5000/getCart").json()["items"]
# print(cart_list)
# time.sleep(1)
# request8 = session.post(url="http://127.0.0.1:5000/placeOrder", json=cart_list)
# request8 = session.get(url="http://127.0.0.1:5000/logout")

