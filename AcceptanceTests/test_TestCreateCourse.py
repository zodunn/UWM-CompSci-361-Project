import django.db.utils
from django.test import TestCase
from ProjectApp.models import Course
from django.test import Client
class TestCreateCourse(TestCase):
    def setUp(self):
        self.client = Client()

    def testCreateCourseSuccess(self):
        response = self.client.post('/home.html/coursecreator.html', {"CourseName": 'Dinosaurs', 'CourseNumber': "321"})
        course = Course.objects.get(number=321)
        self.assertEqual(course.name, "Dinosaurs", msg="New created course does not appear in database")
        a = response.request['PATH_INFO']
        self.assertEqual(a, '/home.html/coursecreator.html', msg="Did not redirect properly to same page")


class TestInvalidCourseName(TestCase):
    def setUp(self):
        self.client = Client()

    def testInvalidCourseName(self):
        response = self.client.post('/home.html/coursecreator.html', {"CourseName": '', 'CourseNumber': "321"}, follow=True)
        a = response.request['PATH_INFO']
        self.assertEqual(a, '/home.html/coursecreator.html',
                         msg="Bad course name during course creation did not redirect to course creator page")


class TestTakenCourseNumber(TestCase):
    def setUp(self):
        self.newCourse = Course(name="Bananas", number=321)
        self.newCourse.save()
        self.client = Client()

    def testTakenCourseNumber(self):
        with self.assertRaises(django.db.utils.IntegrityError, msg="Taken course should not be created"):
            response = self.client.post('/home.html/coursecreator.html', {"CourseName": 'Dinosaurs', 'CourseNumber': "321"}, follow=True)

class TestNegCourseNumber(TestCase):
    def setUp(self):
        self.client = Client()
    def testNegativeCourseNumber(self):
        response = self.client.post('/home.html/coursecreator.html', {"CourseName": 'Dinosaurs', 'CourseNumber': "-321"}, follow=True)
        redirect = response.redirect_chain
        self.assertEqual(0, len(redirect),
                         msg="Negative course number during course creation did not redirect to course creator page")
        self.assertEqual(response.context["message"], "Invalid Course Number",
                         msg="Negative course number did not return correct error message")
        redirect = response.redirect_chain
        self.assertEqual(len(redirect), 0, msg="Did not redirect properly to same page")
