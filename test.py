from app import create_app
import unittest

class ApplicationBaseTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test_get_static_page_contact(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def test_get_static_page_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_get_static_page_about(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()