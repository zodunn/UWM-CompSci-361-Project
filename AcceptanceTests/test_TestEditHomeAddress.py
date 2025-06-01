import enum

from ProjectApp.models import User
from django.test import TestCase
from django.test import Client


class TestEditAddress(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = User(email="spoof@uwm.edu", account_type="TA", first_name="John", last_name="Doe")
        self.new_user.password = "password123"
        self.new_user.phone_number = "123456789"
        self.new_user.address = "5567 orange st"
        self.new_user.save()

    def testEditAddress(self):
        session = self.client.session
        session['user'] = self.new_user.email
        session.save()
        response = self.client.post('/home.html/personalinfoeditor.html',
                                    {'NewAddress': "3400 N Maryland ave, milwaukee, WI, 533211",
                                     'NewPhoneNumber': "9876543210",
                                     'OfficeHoursRoom': "EMS 100", 'OfficeHoursDays': "MW",
                                     'OfficeHoursTimes': "1:00pm-2:00pm",
                                     'Skills': "stuff"}, follow=True)
        self.new_user = User.objects.get(email="spoof@uwm.edu")
        self.assertEqual(self.new_user.address, '3400 N Maryland ave, milwaukee, WI, 533211', msg="Changed address was not updated")
        redirect = response.request['PATH_INFO']
        self.assertEqual(redirect, '/home.html/personalinfoeditor.html', msg="Did not redirect properly")


class TestEditInvalidAddress(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = User(email="spoof@uwm.edu", account_type="TA", first_name="John", last_name="Doe")
        self.new_user.password = "password123"
        self.new_user.phone_number = "123456789"
        self.new_user.address = "5567 orange st"
        self.new_user.save()

    def testInvalid(self):
        session = self.client.session
        session['user'] = self.new_user.email
        session.save()
        response = self.client.post('/home.html/personalinfoeditor.html',
                                    {'NewAddress': "123",
                                     'NewPhoneNumber': "9876543210",
                                     'OfficeHoursRoom': "EMS 100", 'OfficeHoursDays': "MW",
                                     'OfficeHoursTimes': "1:00pm-2:00pm",
                                     'Skills': "stuff"}, follow=True)
        self.new_user = User.objects.get(email="spoof@uwm.edu")
        self.assertEqual("5567 orange st", self.new_user.address,
                         msg="Invalid address change should not update")
        self.assertEqual(response.context["message"], "An error was found -- please try again",
                         msg="Invalid address did not return correct error message")
        redirect = response.redirect_chain
        self.assertEqual(len(redirect), 0, msg="Did not redirect properly to same page")
