from ProjectApp.models import Section, Course, SectionToCourse
from django.test import TestCase
from django.test import Client
from classes.section_class import SectionType
from classes.new_user_class import AccountType
from ProjectApp.models import User


class TestChangeClassTime(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_section = Section(section_type=SectionType.LAB.name, number=123456, location="EMS 120",
                                   start_time="1:00", end_time="2:00", week_days="MW")
        self.new_section.save()
        self.new_user = User(first_name="John", last_name="Doe", account_type=AccountType.TA, email="spoof@uwm.edu")
        self.new_user2 = User(first_name="Jane", last_name="Doe", account_type=AccountType.SUPERVISOR,
                              email="jdoe@uwm.edu")
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

    def testChangeClassTime(self):
        response = self.client.post('/home.html/supersectioneditor.html',
                                    {'NewDays': self.new_section.week_days, 'NewEndTime': "3:00",
                                     'NewStartTime': "2:00",
                                     'NewSectionNumber': self.new_section.number,
                                     'NewClassroom': self.new_section.location, 'NewTA': self.new_user.email},
                                    follow=True)
        a = response.request['PATH_INFO']
        self.new_section = Section.objects.get(number=123456)
        self.assertEqual(self.new_section.start_time, "2:00", msg="Start time did not update")
        self.assertEqual(self.new_section.end_time, "3:00", msg="End time did not update")
        self.assertEqual('/home.html/supersectioneditor.html', a, msg="Changing Classroom time did not redirect")


class TestChangeClassTimeNoInput(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_section = Section(section_type=SectionType.LAB.name, number=123456, location="EMS 120",
                                   start_time="1:00", end_time="2:00", week_days="MW")
        self.new_section.save()
        self.new_user = User(first_name="John", last_name="Doe", account_type=AccountType.TA, email="spoof@uwm.edu")
        self.new_user2 = User(first_name="Jane", last_name="Doe", account_type=AccountType.SUPERVISOR,
                              email="jdoe@uwm.edu")
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

    def testChangeClassTimeStartEmpty(self):
        try:
            self.client.post('/home.html/supersectioneditor.html',
                                        {'NewDays': self.new_section.week_days, 'NewEndTime': "3:00",
                                        'NewStartTime': "",
                                        'NewSectionNumber': self.new_section.number,
                                        'NewClassroom': self.new_section.location, 'NewTA': self.new_user.email},
                                        follow=True)
        except:
            self.assertEqual("1:00", self.new_section.start_time, msg="Start time updated when it shouldnt")

    def testChangeClassTimeEndEmpty(self):
        session = self.client.session
        session['sectionedit'] = self.new_section.id
        session.save()
        try:
            self.client.post('/home.html/supersectioneditor.html',
                                        {'NewDays': self.new_section.week_days, 'NewEndTime': "",
                                        'NewStartTime': "1:00",
                                        'NewSectionNumber': self.new_section.number,
                                        'NewClassroom': self.new_section.location, 'NewTA': self.new_user.email},
                                        follow=True)
        except:
            self.assertEqual("2:00", self.new_section.end_time, msg="End time updated when it shouldnt")



