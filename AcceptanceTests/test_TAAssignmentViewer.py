from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.test import Client
from ProjectApp.models import Course, User, TAToCourse
from classes.new_user_class import AccountType


class TestViewSchedule(TestCase):
    def setUp(self):
        self.client = Client()
        self.dinoCourse = Course(name="Dinosaurs", number=123)
        self.dinoCourse.save()
        self.mathCourse = Course(name="Math", number=444)
        self.mathCourse.save()
        self.engCourse = Course(name="English", number=228)
        self.engCourse.save()
        self.new_user = User(first_name="John", last_name="Doe", account_type=AccountType.TA, email="spoof@uwm.edu")
        self.new_user.save()
        self.taToCourseObj = TAToCourse(ta=self.new_user, course=self.dinoCourse)
        self.taToCourseObj.save()

        self.courseList = [self.dinoCourse, self.engCourse, self.mathCourse]

    def testViewSchedule(self):
        response = self.client.get('/home.html/coursesschedule.html')
        courses = response.context['courses']
        taToCoursesList = response.context['tasInCourse']
        self.assertEqual(self.taToCourseObj, taToCoursesList[0], msg="should return list of tas for course")
        j = 0
        for i in courses:
            self.assertEqual(i, self.courseList[j])
            j += 1
