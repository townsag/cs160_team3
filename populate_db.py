import db

db.insert_user("AdminAndy", "password123", "One Washington Square, San José, CA 95192", True)

db.insert_category("Fruits") #id 1
db.insert_category("Protein") # id 2
db.insert_category("Nuts") # id 3

db.insert_tag("Gluten Free") # id 1
db.insert_tag("Vegetarian") # id 2
db.insert_tag("Vegan") # id 3

db.insert_product("Apple", "This is a healthy fruit", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTN2Hgg8YOw4ntI9XZl0XX4ppf2VmSYyMrwJjFJhpYJrMeMt6y0XcMqdrQwUytsYfMldkI&usqp=CAU", 100, 19.99, 5.51, 1, [1, 2, 3])
db.insert_product("Almonds", "This is a healthy nut", "https://www.healthysupplies.co.uk/pics/almonds-catpic21.jpg", 50, 23.99, 6.17, 3, [3])

