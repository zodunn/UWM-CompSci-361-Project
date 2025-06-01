import enum

from django.test import TestCase
from django.test import Client
from ProjectApp.models import User


class AccountType(enum.Enum):
    TA = 1
    Instructor = 2
    Supervisor = 3


class TestSendEmail(TestCase):
    def setUp(self):
        self.client = Client()

    def testEmail(self):
        response = self.client.post('/notification/', {"Recipients": "spoof@uwm.edu", 'Title': "Hi", 'Message': "woof"})
        self.assertEqual(response.context["message"], "Email sent!", msg="Email sent should prompt right message")
        redirect = response.redirect_chain
        self.assertEqual(0, len(redirect), msg="Did not redirect to correct same page")


class TestSendInvalidRecipient(TestCase):
    def setUp(self):
        self.client = Client()

    def testRecip(self):
        response = self.client.post('/notification/', {"Recipients": "", 'Title': "Hi", 'Message': "woof"})
        self.assertEqual(response.context["message"], "Email does not have recipients, add some",
                         msg="No email address for sending email did not return correct error message")
        redirect = response.redirect_chain
        self.assertEqual(0, len(redirect), msg="Did not redirect to correct same page")


class TestSendInvalidSubject(TestCase):
    def setUp(self):
        self.client = Client()

    def testSubject(self):
        response = self.client.post('/notification/', {"Recipients": "spoof@uwm.edu", 'Title': "", 'Message': "woof"})
        self.assertEqual(response.context["message"], "Email does not have subject, add one",
                         msg="No subject for sending email did not return correct error message")
        redirect = response.redirect_chain
        self.assertEqual(0, len(redirect), msg="Did not redirect to correct same page")


class TestSendInvalidMessage(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User("boyl@uwm.edu", AccountType(3), "John", "Boyland")
        self.new_user = User("spoof@uwm.edu", AccountType(1), "John", "Doe")

    def testMessage(self):
        response = self.client.post('/notification/', {"Recipients": "spoof@uwm.edu", 'Title': "Hi", 'Message': ""})
        self.assertEqual(response.context["message"], "Email does not have message, add one",
                         msg="No message for sending email did not return correct error message")
        redirect = response.redirect_chain
        self.assertEqual(0, len(redirect), msg="Did not redirect to correct same page")
