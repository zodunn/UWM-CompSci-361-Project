import enum

from django.test import TestCase
from django.test import Client
from ProjectApp.models import User


class AccountType(enum.Enum):
    TA = 1
    Instructor = 2
    Supervisor = 3


class TestValidLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = User("spoof@uwm.edu", AccountType(1), "John", "Doe")
        self.new_user.password = "password123"
        self.new_user.save()

    def Login(self):
        response = self.client.post('/login/', {'Username': "spoof@uwm.edu", 'Password': "password123"}, follow=True)
        redirect = response.redirect_chain
        self.assertEqual("/home/", redirect[0][0], msg="Valid user login did not redirect to home page")


class TestBadPassword(TestCase):
    def setup(self):
        self.client = Client()
        self.new_user = User("spoof@uwm.edu", AccountType(1), "John", "Doe")
        self.new_user.password = "password123"
        self.new_user.save()

    def password(self):
        response = self.client.post('/login/', {'Username': "spoof@uwm.edu", 'Password': "password321"}, follow=True)
        redirect = response.redirect_chain
        self.assertEqual(0, len(redirect), msg="Bad password during login did not redirect to login page")
        self.assertEqual(response.context["message"], "Incorrect username or password",
                         msg="Bad password did not return correct error message")


class TestBadEmail(TestCase):
    def setup(self):
        self.client = Client()
        self.new_user = User("spoof@uwm.edu", AccountType(1), "John", "Doe")
        self.new_user.password = "password123"
        self.new_user.save()

    def testBadEmail(self):
        response = self.client.post('', {"Username": "spoof@uwm.edu", "Password": "password123"}, follow=True)
        redirect = response.redirect_chain
        self.assertEqual(0, len(redirect), msg="Bad email during login did not redirect to login page")
        self.assertEqual(response.context["message"], "Incorrect username or password",
                         msg="Bad email did not return correct error message")


class TestNoEmail(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = User("spoof@uwm.edu", AccountType(1), "John", "Doe")
        self.new_user.password = "password123"
        self.new_user.save()

    def testNoEmail(self):
        response = self.client.post('', {"Username": "", "Password": "password123"}, follow=True)
        redirect = response.redirect_chain
        self.assertEqual(0, len(redirect), msg="No email during login did not redirect to login page")
        self.assertEqual(response.context["message"], "Incorrect username or password",
                         msg="No email did not return correct error message")


class TestNoPassword(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = User("spoof@uwm.edu", AccountType(1), "John", "Doe")
        self.new_user.password = "password123"
        self.new_user.save()

    def testNoPassword(self):
        response = self.client.post('', {"Username": "", "Password": ""}, follow=True)
        redirect = response.redirect_chain
        self.assertEqual(0, len(redirect), msg="No password during login did not redirect to login page")
        self.assertEqual(response.context["message"], "Incorrect username or password",
                         msg="No password did not return correct error message")
