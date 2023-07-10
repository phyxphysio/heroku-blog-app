import unittest
from flask import Flask
from main import app, db, User, BlogPost, Comment

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Set up a temporary in-memory database for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

        # Create a test user
        test_user = User(id=1, name='Test User', email='test@example.com', password='password')
        db.session.add(test_user)

        # Create a test blog post
        test_post = BlogPost(title='Test Post', subtitle='Test Subtitle', date='2023-07-10', body='Test Body', img_url='test.jpg', author=test_user)
        db.session.add(test_post)

        # Create a test comment
        test_comment = Comment(text='Test Comment', comment_author=test_user, parent_post=test_post)
        db.session.add(test_comment)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Liam's Blog", response.data)

    def test_register_route(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Register", response.data)

    def test_login_route(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_logout_route(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_show_post_route(self):
        response = self.app.get('/post/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Post", response.data)

    def test_about_route(self):
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"About", response.data)

    def test_contact_route(self):
        response = self.app.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Contact", response.data)

    #In this test case, the user is not an admin 
    def test_new_post_route(self):
            response = self.app.get('/new-post')
            self.assertEqual(response.status_code, 403)

    #In this test case, the user is not an admin 
    def test_edit_post_route(self):
        response = self.app.get('/edit-post/1')
        self.assertEqual(response.status_code, 403)
            
    #In this test case, the user is not an admin 
    def test_delete_post_route(self):
        response = self.app.get('/delete/1')
        self.assertEqual(response.status_code, 403) 

with app.app_context():
    unittest.main()

