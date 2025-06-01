from django.test import TestCase
from django.test import Client
from ProjectApp.models import User
from classes.new_user_class import AccountType


class TestUpdateOfficeHours(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = User(first_name="John", last_name="Doe", account_type="Instructor", email="spoof@uwm.edu")
        self.new_user.phone_number = "0123456789"
        self.new_user.save()

    def testUpdateOfficeHours(self):
        session = self.client.session
        session['user'] = self.new_user.email
        session.save()
        response = self.client.post('/home.html/personalinfoeditor.html', {'NewAddress': "3400 N Maryland ave, milwaukee 533211",
                                                                      'NewPhoneNumber': "7155318531",
                                                                      'OfficeHoursRoom': "EMS 100", 'OfficeHoursDays': "MW",
                                                                      'OfficeHoursTimes': "1:00pm-2:00pm",
                                                                      'Skills': "stuff"})
        path = response.request['PATH_INFO']
        self.assertEqual(path, '/home.html/personalinfoeditor.html', msg='should go to homepage')
        new_user = User.objects.get(email="spoof@uwm.edu")
        self.assertEqual(new_user.office_hours_room, "EMS 100")
        self.assertEqual(new_user.office_hours_times, "1:00pm-2:00pm")
        self.assertEqual(new_user.office_hours_days, "MW")
