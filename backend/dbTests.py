import unittest
import db

class TestDatabaseFunctions(unittest.TestCase):

    def test_insert_and_select_product(self):
        product_data = {
            'name': 'Test Product',
            'description': 'This is a test product',
            'image': 'test.jpg',
            'quantity': 10,
            'price': 19.99,
            'weight': 2.5,
            'category_id': 1,
            'tags': [1, 2]
        }

        product_id = db.insert_product(**product_data)

        retrieved_product = db.select_product(product_id)
        self.assertEqual(retrieved_product['name'], 'Test Product')
        self.assertEqual(retrieved_product['quantity'], 10)
        # Add more assertions for other attributes

    def test_update_product(self):
        product_data = {
            'name': 'Updated Product',
            'description': 'Updated product description',
            'image': 'updated.jpg',
            'quantity': 5,
            'price': 29.99,
            'weight': 3.0,
            'category_id': 2,
            'tags': [2, 3]
        }

        product_id = db.insert_product(**product_data)

        updated_data = {
            'name': 'New Name',
            'description': 'New description',
            'image': 'new.jpg',
            'quantity': 15,
            'price': 39.99,
            'weight': 4.0,
            'category_id': 3,
            'tags': [3, 4]
        }

        updated_product = db.update_product(product_id, **updated_data)

        self.assertEqual(updated_product['name'], 'New Name')
        self.assertEqual(updated_product['quantity'], 15)
        # Add more assertions for other attributes

    def test_insert_and_select_category(self):
        category_data = {
            'name': 'Test Category'
        }

        category_id = db.insert_category(**category_data)

        retrieved_category = db.select_category(category_id)
        self.assertEqual(retrieved_category['name'], 'Test Category')

if __name__ == '__main__':
    unittest.main()
