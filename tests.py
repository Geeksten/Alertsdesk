import unittest
from server import index, app

# integration tests vs function tests


class MyFlaskIntegrationsTests(unittest.TestCase):
    """This test that we get to the home page"""
    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        result = self.client.get("/")
        self.assertIn("here", result.data)
        self.assertEqual(result.status_code, 200)
        print dir(result)


if __name__ == "__main__":
    unittest.main()
