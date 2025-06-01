from django.test import TestCase
from django.test import Client
from ProjectApp.models import User


class TestChangePhone(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = User("spoof@uwm.edu", "TA", "John", "Doe")
        self.new_user.save()

    def testChange(self):
        session = self.client.session
        session['user'] = self.new_user.email
        session.save()
        response = self.client.post('/home.html/personalinfoeditor.html', {'NewAddress': "3400 N Maryland ave, milwaukee 533211",
                                                                           'NewPhoneNumber': "9876543210",
                                                                           'OfficeHoursRoom': "EMS 100", 'OfficeHoursDays': "MW",
                                                                           'OfficeHoursTimes': "1:00pm-2:00pm",
                                                                           'Skills': "stuff"}, follow=True)
        self.new_user = User.objects.get(email="spoof@uwm.edu")
        self.assertEqual(self.new_user.phone_number, '9876543210', msg="Changed phone number was not updated")
        redirect = response.request['PATH_INFO']
        self.assertEqual(redirect, '/home.html/personalinfoeditor.html', msg="Did not redirect properly")


class TestInvalidChangePhone(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = User("spoof@uwm.edu", "TA", "John", "Doe")
        self.new_user.phone_number = "123456789"
        self.new_user.save()

    def testInvalid(self):
        session = self.client.session
        session['user'] = self.new_user.email
        session.save()
        response = self.client.post('/home.html/personalinfoeditor.html', {'NewAddress': "3400 N Maryland ave, milwaukee 533211",
                                                                           'NewPhoneNumber': "orange juice",
                                                                           'OfficeHoursRoom': "EMS 100", 'OfficeHoursDays': "MW",
                                                                           'OfficeHoursTimes': "1:00pm-2:00pm",
                                                                           'Skills': "stuff"}, follow=True)
        self.new_user = User.objects.get(email="spoof@uwm.edu")
        self.assertEqual("123456789", self.new_user.phone_number, msg="Invalid phone number change should not update")
        redirect = response.request['PATH_INFO']
        self.assertEqual(redirect, '/home.html/personalinfoeditor.html', msg="Did not redirect properly")


class TestChangePhoneSame(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = User("spoof@uwm.edu", "TA", "John", "Doe")
        self.new_user.phone_number = "123456789"
        self.new_user.save()

    def testChangePhoneSame(self):
        session = self.client.session
        session['user'] = self.new_user.email
        session.save()
        response = self.client.post('/home.html/personalinfoeditor.html', {'NewAddress': "3400 N Maryland ave, milwaukee 533211",
                                                                           'NewPhoneNumber': "123456789",
                                                                           'OfficeHoursRoom': "EMS 100", 'OfficeHoursDays': "MW",
                                                                           'OfficeHoursTimes': "1:00pm-2:00pm",
                                                                           'Skills': "stuff"}, follow=True)
        self.new_user = User.objects.get(email="spoof@uwm.edu")
        self.assertEqual("123456789", self.new_user.phone_number, msg="Invalid phone number change should not update")
        redirect = response.request['PATH_INFO']
        self.assertEqual(redirect, '/home.html/personalinfoeditor.html', msg="Did not redirect properly")
