import db

db.insert_user("AdminAndy", "password123", "One Washington Square, San José, CA 95192", True)

db.insert_category("Fruits") #id 1
db.insert_category("Protein") # id 2
db.insert_category("Nuts") # id 3
db.insert_category("Vegetable") # id 4

db.insert_tag("Gluten Free") # id 1
db.insert_tag("Vegetarian") # id 2
db.insert_tag("Vegan") # id 3

db.insert_product("Apple", "This is a healthy fruit", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTN2Hgg8YOw4ntI9XZl0XX4ppf2VmSYyMrwJjFJhpYJrMeMt6y0XcMqdrQwUytsYfMldkI&usqp=CAU", 100, 19.99, 5.51, 1, [1, 3])
db.insert_product("Almonds", "This is a healthy nut", "https://www.healthysupplies.co.uk/pics/almonds-catpic21.jpg", 50, 23.99, 6.17, 3, [3])
db.insert_product("Eggplant", "This is a healthy vegetable", "https://mucci-production-user-uploads-bucket.s3.amazonaws.com/images/Product-IMG_MiniEggplant-rev.original.png", 50, 23.99, 6.17, 4, [1])
db.insert_product("Banana", "This is a healthy fruit", "https://th-thumbnailer.cdn-si-edu.com/4Nq8HbTKgX6djk07DqHqRsRuFq0=/1000x750/filters:no_upscale()/https://tf-cmsv2-smithsonianmag-media.s3.amazonaws.com/filer/d5/24/d5243019-e0fc-4b3c-8cdb-48e22f38bff2/istock-183380744.jpg", 50, 23.99, 6.17, 1, [1])
db.insert_product("Beef", "This is a healthy protein", "https://images.inc.com/uploaded_files/image/1920x1080/getty_80116649_344560.jpg", 50, 23.99, 6.17, 2, [1])
db.insert_product("Cheese", "This is a healthy protein", "https://cdn.britannica.com/60/217660-050-DBCC409A/cheddar-cheese-wedge.jpg", 50, 23.99, 6.17, 2, [1])
db.insert_product("Chicken", "This is a healthy protein", "https://images.eatthismuch.com/img/395_ldementhon_471464da-daad-4a92-8b5d-7e9a6de898a8.png", 50, 23.99, 6.17, 2, [1])
db.insert_product("Walnuts", "This is a healthy nut", "https://cdn.britannica.com/69/124169-050-54860BD1/fruit-walnut-tree-husk.jpg", 50, 23.99, 6.17, 3, [1])
