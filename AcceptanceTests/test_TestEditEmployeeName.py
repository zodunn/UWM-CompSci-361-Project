import enum

from django.test import TestCase
from django.test import Client
from ProjectApp.models import User
from classes.new_user_class import AccountType


class TestEditFName(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = User(email="spoof@uwm.edu", account_type=AccountType, first_name="John", last_name="Doe")
        self.new_user.save()
        session = self.client.session
        session['accountedit'] = self.new_user.email
        session['user'] = self.new_user.email
        session.save()

    def testFirstName(self):
        response = self.client.post('/home.html/accounteditor.html', {"UserFirstName": 'Jimmy', "UserLastName": 'Doe'}, follow=True)
        self.new_user = User.objects.get(email = "spoof@uwm.edu")
        self.assertEqual(self.new_user.first_name, 'Jimmy', msg="Changed first name was not updated")
        a = response.request['PATH_INFO']
        self.assertEqual(a, '/home.html/accounteditor.html', msg="Did not redirect to correct page")


class TestEditInvalidFName(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = User(email="spoof@uwm.edu", account_type=AccountType.TA, first_name="John", last_name="Doe")
        self.new_user.save()
        session = self.client.session
        session['accountedit'] = self.new_user.email
        session['user'] = self.new_user.email
        session.save()

    def testInvalidFirstName(self):
        response = self.client.post('/home.html/accounteditor.html', {"UserFirstName": "", "UserLastName": "Doe"}, follow=True)
        self.new_user = User.objects.get(email = "spoof@uwm.edu")
        self.assertEqual("John", self.new_user.first_name, msg="Invalid first name change should not update")
        self.assertEqual(response.context["message"], "Invalid First Name",
                         msg="Invalid first name did not return correct error message")
        redirect = response.redirect_chain
        self.assertEqual(0, len(redirect), msg="Did not redirect to same page")


class TestEditLName(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = User(email="spoof@uwm.edu", account_type=AccountType.TA, first_name="John", last_name="Doe")
        self.new_user.save()
        session = self.client.session
        session['accountedit'] = self.new_user.email
        session['user'] = self.new_user.email
        session.save()

    def testLastName(self):
        response = self.client.post('/home.html/accounteditor.html', {"UserFirstName":"John", "UserLastName": 'Jimmy'}, follow=True)
        self.new_user = User.objects.get(email = "spoof@uwm.edu")
        self.assertEqual(self.new_user.last_name, 'Jimmy', msg="Changed last name was not updated")
        a = response.request['PATH_INFO']
        self.assertEqual(a, '/home.html/accounteditor.html', msg="Did not render correct URL")


class TestEditInvalidLName(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = User("spoof@uwm.edu", "Instructor", "John", "Doe")
        self.new_user.save()
        session = self.client.session
        session['accountedit'] = self.new_user.email
        session['user'] = self.new_user.email
        session.save()

    def testInvalidLastName(self):
        response = self.client.post('/home.html/accounteditor.html', {"UserFirstName": "John", "UserLastName": ""},
                                    follow=True)
        self.new_user = User.objects.get(email="spoof@uwm.edu")
        self.assertEqual("Doe", self.new_user.last_name, msg="Invalid first name change should not update")

        redirect = response.request['PATH_INFO']
        self.assertEqual(redirect, "/home.html/accounteditor.html", msg="Did not redirect to same page")


