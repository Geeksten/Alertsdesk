import unittest
from server import index, app, User
from model import db, connect_to_db, User
from flask import session, request

# integration tests vs function tests


class MyFlaskIntegrationsTests(unittest.TestCase):
    """This tests that we get to the home page"""
    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        result = self.client.get("/")
        self.assertIn("here", result.data)
        # self.assertEqual(result.status_code, 404)
        self.assertEqual(result.status_code, 200)
        print dir(result)


class MyAlertsdeskDBTests(unittest.TestCase):
    """This tests that a new user is registers successfully and is added to test database"""
    def setUp(self):
        print "connecting to db"
        connect_to_db(app)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()
        self.client = app.test_client()
        # adding the following line will make sure you can test find as well

    def tearDown(self):
        print "doing my teardown"
        User.query.filter_by(firstname="wilma").delete
        db.session.commit()

    def test_add_user(self):
        newuser = User(firstname="wilma", lastname="smith", email='wilma@example.com', password='password')
        db.session.add(newuser)
        db.session.commit()
        mm = User.query.filter_by(firstname="wilma").first()
        self.assertEqual(mm.firstname, "wilma")

#############################################################################

if __name__ == "__main__":
    unittest.main()
