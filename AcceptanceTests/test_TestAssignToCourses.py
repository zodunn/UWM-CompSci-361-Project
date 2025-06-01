import enum

from ProjectApp.models import Course, User
from django.test import TestCase
from django.test import Client
from classes.new_user_class import AccountType, Category, PersonalInfoCategory

class TestAssignInstructor(TestCase):
    def setUp(self):
        self.client = Client()
        self.dinoCourse = Course(name="Dinosaurs", number=123)
        self.dinoCourse.save()
        self.mathCourse = Course(name="Math", number=321)
        self.mathCourse.save()
        self.new_user = User(first_name="John", last_name="Doe", account_type=AccountType.INSTRUCTOR, email="spoof@uwm.edu")
        self.new_user.save()
        self.courseList = {self.mathCourse, self.dinoCourse}

    def testAssignInstructor(self):
        session = self.client.session
        session['courseedit'] = self.dinoCourse.number
        session.save()
        response = self.client.post('/home.html/courseeditor.html', {'NewName':self.dinoCourse.name, 'ConfirmChanges':'ConfirmChanges', 'Instructor':self.new_user.email}, follow=True)
        self.assertEqual(response.context['message'], "Changes Successfully Saved!")
        redirect = response.redirect_chain
        self.assertEqual(0, len(redirect), msg="Did not redirect to correct same page")
