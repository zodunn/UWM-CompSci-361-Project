from django.test import TestCase
from django.test import Client
from classes.new_user_class import AccountType
from ProjectApp.models import User


class TestNoAccountAccess(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = User(first_name="John", last_name="Doe", account_type=AccountType.INSTRUCTOR, email="spoof@uwm.edu")
        self.new_user.save()

    def testNoAccountAccess(self):
        response = self.client.post('/', {"Username": "thisemailisreal@totallylegit.com", "Password": "a real password for a real user"})
        path = response.request['PATH_INFO']
        self.assertEqual(path, '/', msg="Someone with no permissions should not be able to access site")

    def testBadPassword(self):
        response = self.client.post('/', {"Username": "spoof@uwm.edu", "Password": "a real password for a real user"})
        path = response.request['PATH_INFO']
        self.assertEqual(path, '/', msg="Someone with no permissions should not be able to access site")

    def testBadUserName(self):
        response = self.client.post('/', {"Username": "spoofy@uwm.edu", "Password": "default"})
        path = response.request['PATH_INFO']
        self.assertEqual(path, '/', msg="Someone with no permissions should not be able to access site")