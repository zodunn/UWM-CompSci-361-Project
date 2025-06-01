import enum

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.test import Client

import ProjectApp
from ProjectApp.models import User
from classes.new_user_class import AccountType


class TestDeleteAccount(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = User(email="spoof@uwm.edu", account_type=AccountType.TA, first_name="John", last_name="Doe")
        self.new_user2 = User(email="spoofle@uwm.edu", account_type=AccountType.SUPERVISOR, first_name="Jane", last_name="Doe")

        self.new_user.save()
        self.new_user2.save()
        session = self.client.session
        session['accountdelete'] = self.new_user.email
        session['user'] = self.new_user2.email
        session.save()

    def testDeleteAccount(self):
        response = self.client.post('/home.html/accountdeletion.html', {'Delete':"", }, follow=True)
        with self.assertRaises(ProjectApp.models.User.DoesNotExist, msg="After deletion should not find user in db"):
            User.objects.get(email="spoof@uwm.edu")
        a = response.request['PATH_INFO']
        self.assertEqual(a, '/home.html/PCIviewer.html', msg="Deleting an account didn't redirect to the PCI viewer")