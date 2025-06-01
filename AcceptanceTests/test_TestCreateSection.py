import enum

from django.test import TestCase
from django.test import Client
from ProjectApp.models import User, Course, Section


class AccountType(enum.Enum):
    TA = 1
    Instructor = 2
    Supervisor = 3


class TestCreateValidSection(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User("boyl@uwm.edu", AccountType(3), "John", "Boyland")
        self.dinoCourse = Course("Dinosaurs", 123)
        self.mathCourse = Course(name="Math", number=321)
        self.mathCourse.save()
        self.admin_user.save()
        self.dinoCourse.save()
        session = self.client.session
        session['courseToGetSectionsOf'] = self.mathCourse.number
        session['addSectionToCourse'] = self.mathCourse.number
        session.save()

    def testSuccess(self):
        response = self.client.post('/home.html/sectioncreator.html',
                                    {'SectionNumber': "123456", 'Classroom': "EMS 120", 'sectionType': "Lab",
                                     'StartTime': "1:00pm", 'EndTime': "2:00pm", 'Days': "MW"}, follow=True)
        section = Section.objects.get(number=123456)
        self.assertEqual(section.location, "EMS 120",
                         msg="Created section does not have correct classroom in database")
        a = response.request['PATH_INFO']
        self.assertEqual(a, "/home.html/sectioncreator.html",
                         msg="Properly creating a section did not redirect properly")

class TestBadSectionNumber(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User("boyl@uwm.edu", AccountType(3), "John", "Boyland")
        self.dinoCourse = Course("Dinosaurs", 123)
        self.admin_user.save()
        self.dinoCourse.save()
        session = self.client.session
        session['courseToGetSectionsOf'] = self.dinoCourse.number
        session['addSectionToCourse'] = self.dinoCourse.number
        session.save()

    def testBadSectionNumber(self):
        response = self.client.post('/home.html/sectioncreator.html',
                                    {'SectionNumber': "poopy", 'Classroom': "EMS 120", 'sectionType': "Lab",
                                     'StartTime': "1:00pm", 'EndTime': "2:00pm", 'Days': "MW"}, follow=True)
        a = response.request['PATH_INFO']
        self.assertEqual(a, "/home.html/sectioncreator.html",
                         msg="Properly creating a section did not redirect properly")
        self.assertEqual(response.context["message"], "Invalid Section Number",
                         msg="Bad section number did not return correct error message")


class TestBadSectionClassroom(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User("boyl@uwm.edu", AccountType(3), "John", "Boyland")
        self.dinoCourse = Course("Dinosaurs", 123)
        self.admin_user.save()
        self.dinoCourse.save()

    def testBadSectionClassroom(self):
        response = self.client.post('/home.html/sectioncreator.html',
                                    {'SectionNumber': "123456", 'Classroom': "", 'default': "Lab",
                                     'StartTime': "1:00pm", 'EndTime': "2:00pm", 'Days': "MW"}, follow=True)
        a = response.request['PATH_INFO']
        self.assertEqual(a, "/home.html/sectioncreator.html",
                         msg="Improperly creating a section did not redirect properly")
        self.assertEqual(response.context["message"], "Invalid Section Classroom",
                         msg="Bad section classroom did not return correct error message")


class TestBadSectionType(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User("boyl@uwm.edu", AccountType(3), "John", "Boyland")
        self.dinoCourse = Course("Dinosaurs", 123)
        self.admin_user.save()
        self.dinoCourse.save()

    def testBadSectionType(self):
        response = self.client.post('/home.html/sectioncreator.html',
                                    {'SectionNumber': "123456", 'Classroom': "EMS 120", 'sectionType': "",
                                     'StartTime': "1:00pm", 'EndTime': "2:00pm", 'Days': "MW"}, follow=True)
        a = response.request['PATH_INFO']
        self.assertEqual(a, "/home.html/sectioncreator.html",
                         msg="Improperly creating a section did not redirect properly")
        self.assertEqual(response.context["message"], "Invalid Section Type",
                         msg="Bad section type did not return correct error message")
