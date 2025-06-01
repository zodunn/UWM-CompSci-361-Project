from ProjectApp.models import User, Course
from django.test import TestCase
from django.test import Client
from classes.new_user_class import AccountType


class TestViewCourseAssignments(TestCase):
    def setUp(self):
        self.client = Client()
        self.dinoCourse = Course(name="Dinosaurs", number=123)
        self.dinoCourse.save()
        self.astroCourse = Course(name="asteroids", number=569)
        self.astroCourse.save()

        self.new_user = User(first_name="John", last_name="Doe", account_type=AccountType.INSTRUCTOR, email="spoof@uwm.edu")
        self.new_user.save()

        self.dinoCourse.instructor = self.new_user
        self.dinoCourse.save()
        self.astroCourse.instructor = self.new_user
        self.astroCourse.save()

        self.courseList = [self.dinoCourse, self.astroCourse]

    def testViewCourseAssignment(self):
        session = self.client.session
        session['user'] = self.new_user.email
        session.save()
        response = self.client.get('/home.html/course.html/')
        user = response.context['user']
        courses = response.context['courses']
        self.assertEqual(user, self.new_user, msg="user should have been passed to template")
        j = 0
        for i in courses:
            self.assertEqual(i, self.courseList[j], msg="all courses should have been passed to template")
            j += 1


class TestCourseInterfaceButtons(TestCase):
    def setUp(self):
        self.client = Client()
        self.dinoCourse = Course(name="Dinosaurs", number=123)
        self.dinoCourse.save()
        self.astroCourse = Course(name="asteroids", number=569)
        self.astroCourse.save()

        self.new_user = User(first_name="John", last_name="Doe", account_type=AccountType.INSTRUCTOR, email="spoof@uwm.edu")
        self.new_user.save()

    def testViewSections(self):
        session = self.client.session
        session['user'] = self.new_user.email
        session.save()
        response = self.client.post('/home.html/course.html/', {"123": "View Sections"}, follow=True)
        path = response.redirect_chain[0][0]
        self.assertEqual(path, "/home.html/section.html", msg="button should take you to section interface")

    def testEditCourse(self):
        session = self.client.session
        session['user'] = self.new_user.email
        session.save()
        response = self.client.post('/home.html/course.html/', {"123": "Edit Course Information"}, follow=True)
        path = response.redirect_chain[0][0]
        self.assertEqual(path, "/home.html/courseeditor.html", msg="button should take you to course editor")

    def testDeleteCourse(self):
        session = self.client.session
        session['user'] = self.new_user.email
        session.save()
        response = self.client.post('/home.html/course.html/', {"123": "Delete Course"}, follow=True)
        path = response.redirect_chain[0][0]
        self.assertEqual(path, "/home.html/coursedeletion.html", msg="button should take you to course editor")

    def testCreateCourse(self):
        session = self.client.session
        session['user'] = self.new_user.email
        session.save()
        response = self.client.post('/home.html/course.html/', {'Create': 'Create a Course'}, follow=True)
        path = response.redirect_chain[0][0]
        self.assertEqual(path, "/home.html/coursecreator.html", msg="button should take you to course creator")


