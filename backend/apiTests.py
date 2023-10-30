import unittest
import json
from app import app

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_root_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signup_and_login_routes(self):
        # Sign up a test user
        user_data = {
            'username': 'test_user',
            'password': 'test_password',
            'address': 'test_address',
            'is_admin': False
        }
        response = self.app.post('/signup', json=user_data)
        self.assertEqual(response.status_code, 401)
        
        if response.data != b'Signup Success':
            print(f"Signup failed with response: {response.data.decode()}")
        
        self.assertEqual(response.data, b'User Already exists')

        # Log in with the same test user
        login_data = {
            'username': 'test_user',
            'password': 'test_password',
        }
        response = self.app.post('/login', json=login_data)
        self.assertEqual(response.status_code, 200)
        
        if response.data != b'Success':
            print(f"Login failed with response: {response.data.decode()}")
        
        self.assertEqual(response.data, b'Success')


    def test_get_products_route_authenticated(self):
        # Sign up and log in with a test user (as shown in the previous test)
        # Then make a request to the /getProducts route
        login_data = {
            'username': 'test_user',
            'password': 'test_password',
        }
        self.app.post('/login', json=login_data)  # Log in
        response = self.app.get('/getProducts')
        self.assertEqual(response.status_code, 200)
        products = json.loads(response.data)
        self.assertTrue(isinstance(products, list))
    
if __name__ == '__main__':
    unittest.main()
