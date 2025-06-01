import enum

from django.test import TestCase
from django.test import Client
from ProjectApp.models import User, Section, Course, SectionToCourse
from classes.new_user_class import AccountType
from classes.section_class import SectionType


class TestAssignToSection(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_section = Section(section_type=SectionType.LAB.name, number=123456, location="EMS 120", start_time="1:00", end_time="2:00", week_days="MW")
        self.new_section.save()
        self.new_user = User(first_name="John", last_name="Doe", account_type=AccountType.TA, email="spoof@uwm.edu")
        self.new_user2 = User(first_name="Jane", last_name="Doe", account_type=AccountType.SUPERVISOR, email="jdoe@uwm.edu")
        self.new_user.save()
        self.new_user2.save()
        self.mathCourse = Course(name="Math", number=321)
        self.mathCourse.save()
        SectionToCourse.objects.create(course=self.mathCourse, section=self.new_section)
        session = self.client.session
        session['sectionedit'] = self.new_section.id
        session['user'] = self.new_user2.email
        session['courseToGetSectionsOf'] = self.mathCourse.number
        session.save()

    def testAssignToSection(self):

        response = self.client.post('/home.html/supersectioneditor.html', {'NewDays':self.new_section.week_days, 'NewEndTime':self.new_section.end_time, 'NewStartTime':self.new_section.start_time, 'NewSectionNumber':self.new_section.number, 'NewClassroom':self.new_section.location, 'NewTA':self.new_user.email}, follow=True)
        a = response.request['PATH_INFO']
        self.assertEqual(a, "/home.html/supersectioneditor.html",
                         msg="Assigning TA to section did not work correctly")


class TestAssignNoneToSection(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_section = Section(section_type=SectionType.LAB.name, number=123456, location="EMS 120", start_time="1:00", end_time="2:00", week_days="MW")
        self.new_section.save()
        self.mathCourse = Course(name="Math", number=321)
        self.mathCourse.save()
        SectionToCourse.objects.create(course = self.mathCourse, section=self.new_section)
        self.new_user = User(first_name="John", last_name="Doe", account_type=AccountType.SUPERVISOR, email="spoof@uwm.edu")
        self.new_user.save()
        session = self.client.session
        session['sectionedit'] = self.new_section.id
        session['user'] = self.new_user.email
        session['courseToGetSectionsOf'] = self.mathCourse.number
        session.save()

    def testAssignNoneToSection(self):

        response = self.client.post('/home.html/supersectioneditor.html', {'NewTA': ""})
        a = response.request['PATH_INFO']
        self.assertEqual(a, "/home.html/supersectioneditor.html",
                         msg="Assigning TA to none in section did not work correctly")
