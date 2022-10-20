from unittest import TestCase

from app import app
from models import User, connect_db, db

#DEFAULT_IMAGE_URL

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

connect_db(app)
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            image_url='test1',
        )

        second_user = User(
            first_name="test_first_two",
            last_name="test_last_two",
            image_url='test2',
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """ 
            Test that page successfully loaded, 
            and test_user first_name last_name on page
        """

        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_edit_users(self):
        """
            Test query given user id and render edit page with correct data
        """

        with self.client as c:
            test_user = User.query.get(self.user_id)
            resp = c.get(f"/users/{test_user.id}/edit")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)
            self.assertIn("<!--edit page rendered (comment for testing)-->",html)
            
    
    def test_add_users(self):
        """
            Test adding user and verifying shown on users page.
        """
        with self.client as c:
            data = {
                'first_name':'third',
                'last_name':'added_user',
                'image_url':'test3'
            }
            resp = c.post("/users/new", follow_redirects=True, data=data)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!--display_users page rendered (comment for testing)-->",html)
            self.assertIn("third", html)
            self.assertIn("added_user", html)
            
           

    def test_delete_user(self):
        """
            Test deleting a user with given id and verify they are no longer 
            on the list of users shown on the landing page.
        """
        
        with self.client as c:

            resp = c.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertNotIn("test_first ", html)
            self.assertNotIn("test_last ", html)
