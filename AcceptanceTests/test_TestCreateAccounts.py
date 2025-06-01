import enum

from django.test import TestCase
from django.test import Client
from ProjectApp.models import User


class TestCreateUserAccount(TestCase):
    def setUp(self):
        self.client = Client()

    def testNewUser(self):
        response = self.client.post('/home.html/accountcreator.html',
                                    {"UserFirstName": "John", 'UserLastName': "Doe", "UserEmail": "spoof@uwm.edu",
                                     "UserRole": "Instructor"})
        account = User.objects.get(email="spoof@uwm.edu")
        self.assertEqual(account.first_name, "John", msg="Correct created account was not found in database")
        a = response.request['PATH_INFO']
        self.assertEqual(a, '/home.html/accountcreator.html', msg="Did not redirect to correct page")


class TestInvalidUserName(TestCase):
    def setUp(self):
        self.client = Client()

    def testInvalidUserName(self):
        response = self.client.post('home.html/accountcreator.html', {"UserFirstName": "", 'UserLastName': "Doe",
                                                         "UserEmail": "spoof@uwm.edu", "UserRole": "Instructor"})
        a = response.request['PATH_INFO']
        self.assertEqual(a, 'home.html/accountcreator.html',
                         msg="Bad account name during account creation did not redirect to account creator page")


class TestInvalidUserEmail(TestCase):
    def setUp(self):
        self.client = Client()
    def testInvalidUserName(self):
        response = self.client.post('home.html/accountcreator.html', {"UserFirstName": "John", 'UserLastName': "Doe",
                                                         "UserEmail": "spoof@gmail.com", "UserRole": "Instructor"})
        a = response.request['PATH_INFO']
        self.assertEqual(a, 'home.html/accountcreator.html',
                         msg="Bad account email during account creation did not redirect to account creator page")

class TestInvalidUserType(TestCase):
    def setUp(self):
        self.client = Client()
    def testInvalidUserName(self):
        response = self.client.post('home.html/accountcreator.html', {"UserFirstName": "John", 'UserLastName': "Doe",
                                                         "UserEmail": "spoof@uwm.edu", "UserRole": ""})
        a = response.request['PATH_INFO']
        self.assertEqual(a, 'home.html/accountcreator.html',
                         msg="Bad account type during account creation did not redirect to account creator page")
