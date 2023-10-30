import db

db.insert_user("AdminAndy", "password123", "One Washington Square, San José, CA 95192", True)
db.insert_user("employee1", "123123", "One Washington Square, San José, CA 95192", True)
db.insert_user("customer1", "123123", "One Washington Square, San José, CA 95192", False)

db.insert_category("Fruits") #id 1
db.insert_category("Protein") # id 2
db.insert_category("Nuts") # id 3
db.insert_category("Vegetable") # id 4

db.insert_tag("Gluten Free") # id 1
db.insert_tag("Vegetarian") # id 2
db.insert_tag("Vegan") # id 3
db.insert_tag("Lactose Free")
db.insert_tag("Nut Free")

db.insert_product("Apple", "Fresh and crisp apple, rich in vitamins and fiber", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTN2Hgg8YOw4ntI9XZl0XX4ppf2VmSYyMrwJjFJhpYJrMeMt6y0XcMqdrQwUytsYfMldkI&usqp=CAU", 100, 19.99, 5.51, 1, [1, 3])
db.insert_product("Almonds", "Premium quality almonds, packed with healthy fats and protein", "https://www.healthysupplies.co.uk/pics/almonds-catpic21.jpg", 50, 23.99, 6.17, 3, [3])
db.insert_product("Eggplant", "Organic eggplant, perfect for various culinary delights", "https://mucci-production-user-uploads-bucket.s3.amazonaws.com/images/Product-IMG_MiniEggplant-rev.original.png", 50, 23.99, 6.17, 4, [1])
db.insert_product("Banana", "Sweet and nutritious banana, a great source of energy", "https://th-thumbnailer.cdn-si-edu.com/4Nq8HbTKgX6djk07DqHqRsRuFq0=/1000x750/filters:no_upscale()/https://tf-cmsv2-smithsonianmag-media.s3.amazonaws.com/filer/d5/24/d5243019-e0fc-4b3c-8cdb-48e22f38bff2/istock-183380744.jpg", 50, 23.99, 6.17, 1, [1])
db.insert_product("Beef", "Premium lean beef, a great source of high-quality protein", "https://images.inc.com/uploaded_files/image/1920x1080/getty_80116649_344560.jpg", 50, 23.99, 6.17, 2, [1])
db.insert_product("Cheese", "Aged cheddar cheese, rich in calcium and delicious flavor", "https://cdn.britannica.com/60/217660-050-DBCC409A/cheddar-cheese-wedge.jpg", 50, 23.99, 6.17, 2, [1])
db.insert_product("Chicken", "Premium chicken breast, a versatile and healthy protein option", "https://images.eatthismuch.com/img/395_ldementhon_471464da-daad-4a92-8b5d-7e9a6de898a8.png", 50, 23.99, 6.17, 2, [1])
db.insert_product("Walnuts", "Fresh and crunchy walnuts, high in omega-3 fatty acids", "https://cdn.britannica.com/69/124169-050-54860BD1/fruit-walnut-tree-husk.jpg", 50, 23.99, 6.17, 3, [1])

db.insert_product("Orange", "Sweet and citrusy fruit, lactose-free and nut-free", "", 50, 14.99, 3.3, 1, [1, 3, 4, 5])
db.insert_product("Salmon", "Healthy and delicious fish, lactose-free and nut-free", "", 50, 29.99, 0.75, 2, [2, 3, 4, 5])
db.insert_product("Cashews", "Creamy and crunchy nuts, lactose-free", "", 50, 19.99, 5.1, 3, [1, 4])
db.insert_product("Spinach", "Nutrient-rich leafy green, lactose-free and nut-free", "", 50, 9.99, 0.88, 4, [1, 2, 4, 5])
db.insert_product("Peach", "Juicy and flavorful fruit, lactose-free and nut-free", "", 50, 16.99, 3.8, 1, [1, 3, 4, 5])
db.insert_product("Tofu", "Versatile plant-based protein, lactose-free and nut-free", "", 50, 12.99, 2.2, 2, [2, 3, 4, 5])
db.insert_product("Pistachios", "Delicious and healthy nuts, lactose-free and nut-free", "", 50, 21.99, 5.7, 3, [1, 2, 4, 5])
db.insert_product("Broccoli", "Nutritious cruciferous vegetable, lactose-free and nut-free", "", 50, 8.99, 1.5, 4, [1, 2, 4, 5])
db.insert_product("Mango", "Sweet tropical fruit, lactose-free and nut-free", "", 50, 18.99, 2.8, 1, [1, 3, 4, 5])
db.insert_product("Chickpeas", "Protein-packed legumes, lactose-free and nut-free", "", 50, 7.99, 2.0, 4, [2, 3, 4, 5])

# test shopping cart
db.insert_cart_item(1, 1, 1)
db.insert_cart_item(1, 2, 2)
db.insert_cart_item(1, 3, 3)
db.insert_cart_item(1, 4, 4)
