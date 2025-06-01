from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.test import Client
from ProjectApp.models import User
from classes.new_user_class import AccountType


class TestViewPublicInfoSupervisor(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = User(first_name="John", last_name="Doe", account_type=AccountType.INSTRUCTOR, email="spoof@uwm.edu")
        self.new_user.address = "9907 Potato St, Milwaukee, 53211"
        self.new_user.save()

        self.new_user2 = User(first_name="Jane", last_name="Doe", account_type=AccountType.TA, email="goof@uwm.edu")
        self.new_user2.address = "9907 Potato St, Milwaukee, 53211"
        self.new_user2.save()

        self.new_user3 = User(first_name="John", last_name="Spoon", account_type=AccountType.SUPERVISOR, email="donk@uwm.edu")
        self.new_user3.address = "3400 N Maryland Ave, Milwaukee, 53211"
        self.new_user3.phone_number = "9999888777"
        self.new_user3.save()

    def testViewPublicInfoSupervisorGet(self):
        session = self.client.session
        session['user'] = self.new_user3.email
        session.save()
        response = self.client.get('/home.html/PCIviewer.html')
        users = response.context['users']
        userWhoRequested = response.context['user']
        listOfUsers = User.objects.all()
        j = 0
        for i in users:
            self.assertEqual(i, listOfUsers[j], msg="User was not found so will not show properly in the public info viewer")
            j += 1
        self.assertEqual(userWhoRequested, self.new_user3, msg="user who requested should be supervisor")

    def testViewPublicInfoSupervisorPostEdit(self):
        response = self.client.post('/home.html/PCIviewer.html', {'donk@uwm.edu': 'Edit User Information'}, follow=True)
        path = response.redirect_chain[0][0]
        self.assertEqual(path, 'accounteditor.html', msg="supervisor should be able to edit user info from account viewer")

    def testViewPublicInfoSupervisorPostDelete(self):
        response = self.client.post('/home.html/PCIviewer.html', {'donk@uwm.edu': 'Delete User'}, follow=True)
        path = response.redirect_chain[0][0]
        self.assertEqual(path, 'accountdeletion.html', msg="supervisor should be able to delete user info from account viewer")

    def testViewPublicInfoSupervisorPostCreate(self):
        response = self.client.post('/home.html/PCIviewer.html', {'Create': 'Create a User'}, follow=True)
        path = response.request['PATH_INFO']
        self.assertEqual(path, '/home.html/PCIviewer.html', msg="supervisor should be able to create user info from account viewer")
