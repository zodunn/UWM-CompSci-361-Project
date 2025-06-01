from django.test import TestCase
from ProjectApp.models import Course, Section, User, SectionToCourse, TAToCourse
from classes.course_class import CourseClass
from enum import Enum
import mock

from classes.new_user_class import AccountType


class SectionType(Enum):
    LECTURE = 1
    LAB = 2
    DISCUSSION = 3


class TestCourseSetName(TestCase):  # Void course.setName(course, value)
    def setUp(self):
        self.new_course = Course(name="Course Name", number=123)
        self.new_course.save()

    def test_CourseSetNameValid(self):
        CourseClass.setName(self, self.new_course, "System Programming")
        self.assertEqual(self.new_course.name, "System Programming", "course name should have been changed")

    def test_CourseSetNameInvalid1(self):
        self.assertRaises(TypeError, CourseClass.setName, self, self.new_course, 123, msg="course.setName should raise error if invalid input")

    def test_CourseSetNameInvalid2(self):
        self.assertRaises(TypeError, CourseClass.setName, self, self.new_course, None, msg="course.setName should raise error if invalid input")

    def test_CourseSetNameNoCourseInput(self):
        self.assertRaises(TypeError, CourseClass.setName, self, None, "System Programming", msg="course.setName should raise error if invalid input")

    def test_CourseSetNameBadCourseInput(self):
        self.assertRaises(TypeError, CourseClass.setName, self, "course", "System Programming", msg="course.setName should raise error if invalid input")

class TestCourseGetName(TestCase):  # Void course.getName(course)
    def setUp(self):
        self.new_course = Course(name="Software Engineering", number=361)
        self.new_course.save()

    def test_CourseGetName(self):
        self.assertEqual(CourseClass.getName(self, self.new_course), "Software Engineering", "Two names should be equal")

    def test_CourseGetNameBadInput(self):
        self.assertRaises(TypeError, CourseClass.getName, self, "course", "should raise error for bad input")

    def test_CourseGetNameNoInput(self):
        self.assertRaises(TypeError, CourseClass.getName, self, None, "should raise error for no input")


class TestCourseGetNumber(TestCase):  # Void course.getNumber(course)
    def setUp(self):
        self.new_course = Course(name="Software Engineering", number=361)
        self.new_course.save()

    def test_CourseGetNumber(self):
        self.assertEqual(CourseClass.getNumber(self, self.new_course), 361, "should return course number")

    def test_CourseGetNumberBadInput(self):
        self.assertRaises(TypeError, CourseClass.getNumber, self, "course", "should raise error for bad input")

    def test_CourseGetNumberNoInput(self):
        self.assertRaises(TypeError, CourseClass.getNumber, self, None, "should raise error for no input")


class TestCourseAddSection(TestCase):  # Void course.addSection(course, section)
    def setUp(self):
        self.new_course = Course(name="Software Engineering", number=361)
        self.new_course.save()
        self.new_course2 = Course(name="System Programming", number=337)
        self.new_course2.save()
        self.new_section = Section.objects.create(section_type=SectionType.LECTURE, number = 401, location = "EMS 270", start_time = "2:00:00pm", end_time = "4:00:00pm", week_days="MW")


    def test_CourseAddSectionValid(self):
        CourseClass.addSection(self, self.new_course, self.new_section)
        sectionToCourseObj = SectionToCourse.objects.get(course=self.new_course)
        self.assertEqual(sectionToCourseObj.section, self.new_section, "section should have been added to course")

    def test_CourseAddSectionInvalid(self):
        with self.assertRaises(TypeError, msg="addSection should raise an error if bad input"):
            CourseClass.addSection(self, self.new_course, "section")

    def test_CourseAddSectionNull(self):
        with self.assertRaises(TypeError, msg="addSection should raise an error if no input"):
            CourseClass.addSection(self, self.new_course, None)

    def test_CourseAddSectionDuplicate(self):
        CourseClass.addSection(self, self.new_course, self.new_section)
        with self.assertRaises(RuntimeError, msg="addSection should raise error if section is already added"):
            CourseClass.addSection(self, self.new_course, self.new_section)

    def test_CourseAddSectionAlreadyUsed(self):
        CourseClass.addSection(self, self.new_course, self.new_section)
        with self.assertRaises(RuntimeError, msg="addSection should raise and error if section is already added to a different course"):
            CourseClass.addSection(self, self.new_course2, self.new_section)

    def test_CourseAddSectionBadCourse(self):
        with self.assertRaises(TypeError, msg="add section should raise error if bad course input"):
            CourseClass.addSection(self, "course", self.new_section)

    def test_CourseAddSectionNoCourse(self):
        with self.assertRaises(TypeError, msg="add section should raise error if bad course input"):
            CourseClass.addSection(self, None, self.new_section)


class TestCourseGetSections(TestCase):  # List<Section> course.getSections()
    def setUp(self):
        self.new_course = Course(name="Software Engineering", number=361)
        self.new_course.save()
        self.new_section = Section.objects.create(section_type=SectionType.LECTURE, number=401, location="EMS 270", start_time="2:00:00pm", end_time="4:00:00pm", week_days="MW")
        self.new_section2 = Section.objects.create(section_type=SectionType.LAB, number=402, location="EMS 450", start_time="2:00:00", end_time="6:00:00pm", week_days="M")

        self.sectionToCourseOjb = SectionToCourse(course=self.new_course, section=self.new_section)
        self.sectionToCourseOjb.save()
        self.sectionToCourseObj2 = SectionToCourse(course=self.new_course, section=self.new_section2)
        self.sectionToCourseObj2.save()

    def test_GetSectionsValid(self):
        self.assertEqual(CourseClass.getSections(self, self.new_course), list((self.new_section, self.new_section2)), "getSections should return a list of sections for the course")

    def test_GetSectionsInvalid(self):
        self.assertRaises(TypeError, CourseClass.getSections, self, "course", msg="getSections should raise error for bad input")

    def test_GetSectionsNone(self):
        self.assertRaises(TypeError, CourseClass.getSections, self, None, msg="getSections should raise error for bad input")


class TestCourseAssignInstructor(TestCase):  # Void course.assignInstructor(course, user)
    def setUp(self):
        self.address = "3400 N Maryland Avenue, Milwaukee, WI, 53211"
        self.password = "default_password"
        self.user_supervisor = User.objects.create(email="jndoe@example.com", account_type=AccountType.SUPERVISOR, first_name="Jane", last_name="Doe", address=self.address, phone_number="9998887777", password=self.password)
        self.user_instructor = User.objects.create(email="jkdoe@example.com", account_type=AccountType.INSTRUCTOR, first_name="Jake", last_name="Doe", address=self.address, phone_number="9998887777", password=self.password)
        self.user_TA = User.objects.create(email="jodoe@example.com", account_type=AccountType.TA, first_name="Joe", last_name="Doe", address=self.address, phone_number="9998887777", password=self.password)
        self.new_course = Course(name="Software Engineering", number=361)
        self.new_course.save()

    def test_AssignInstructorSuccess(self):
        CourseClass.assignInstructor(self, self.new_course, self.user_instructor)
        self.assertEqual(self.new_course.instructor, self.user_instructor, "instructor should have been assigned to the course")

    def test_AssignInstructorFail1(self):
        with self.assertRaises(TypeError, msg="type error should have been raised if a ta was assigned as the instructor of a course"):
            CourseClass.assignInstructor(self, self.new_course, self.user_TA)

    def test_AssignInstructorFail2(self):
        with self.assertRaises(TypeError, msg="type error should have been raised if a supervisor was assigned as the instructor of a course"):
            CourseClass.assignInstructor(self, self.new_course, self.user_supervisor)

    def test_AssignInstructorNone(self):
        with self.assertRaises(TypeError, msg="type error should have been raised if no one was assigned"):
            CourseClass.assignInstructor(self, self.new_course, None)

    def test_AssignToBadCourse(self):
        self.assertRaises(TypeError, CourseClass.assignInstructor, self, "course", self.user_instructor, msg="type error should have been raised if bad course input")

    def test_AssignToNoCourse(self):
        self.assertRaises(TypeError, CourseClass.assignInstructor, self, None, self.user_instructor, msg="type error should have been raised if bad course input")


class TestCourseRemoveInstructor(TestCase):  # Void course.removeInstructor()
    def setUp(self):
        self.address = "3400 N Maryland Avenue, Milwaukee, WI, 53211"
        self.password = "default_password"

        self.user_supervisor = User(email="jndoe@example.com", account_type=AccountType.SUPERVISOR, first_name="Jane", last_name="Doe", address=self.address, phone_number="9998887777", password=self.password)
        self.user_supervisor.save()

        self.user_instructor = User(email="jndoe@example.com", account_type=AccountType.INSTRUCTOR, first_name="Jake", last_name="Doe", address=self.address, phone_number="9998887777", password=self.password)
        self.user_instructor.save()

        self.user_TA = User(email="jndoe@example.com", account_type=AccountType.TA, first_name="Joe", last_name="Doe", address=self.address, phone_number="9998887777", password=self.password)
        self.user_TA.save()

        self.new_course = Course(name="Software Engineering", number=361)
        self.new_course.save()

    def test_RemoveInstructorSuccess(self):
        self.new_course.instructor = self.user_instructor
        CourseClass.removeInstructor(self, self.new_course)
        self.assertEqual(self.new_course.instructor, None, "instructor should be removed from course")

    def test_RemoveInstructorNone(self):
        with self.assertRaises(RuntimeError, msg="remove instructor should raise runtime error if there is no instructor to remove"):
            CourseClass.removeInstructor(self, self.new_course)

    def test_RemoveInstructorBadCourseInput(self):
        self.assertRaises(TypeError, CourseClass.removeInstructor, self, "course", msg="remove instructor should raise typeerror if bad input")

    def test_RemoveInstructorNoCourseInput(self):
        self.assertRaises(TypeError, CourseClass.removeInstructor, self, None, msg="remove instructor should raise typeerror if bad input")


class TestCourseAssignTA(TestCase):  # Void course.assignTA(course, user)
    def setUp(self):
        self.address = "3400 N Maryland Avenue, Milwaukee, WI, 53211"
        self.password = "default_password"

        self.user_supervisor = User(email="jndoe@example.com", account_type=AccountType.SUPERVISOR, first_name="Jane", last_name="Doe", address=self.address, phone_number="9998887777", password=self.password)
        self.user_supervisor.save()

        self.user_instructor = User(email="jndoe@example.com", account_type=AccountType.INSTRUCTOR, first_name="Jake", last_name="Doe", address=self.address, phone_number="9998887777", password=self.password)
        self.user_instructor.save()

        self.user_TA = User(email="jndoe@example.com", account_type=AccountType.TA, first_name="Joe", last_name="Doe", address=self.address, phone_number="9998887777", password=self.password)
        self.user_TA.save()

        self.new_course = Course(name="Software Engineering", number=361)
        self.new_course.save()

    def test_AssignTASuccess(self):
        CourseClass.assignTA(self, self.new_course, self.user_TA)
        TAToCourseObj = TAToCourse.objects.get(course=self.new_course)
        self.assertEqual(TAToCourseObj.ta, self.user_TA, "ta should have been assigned to the course")

    def test_AssignTAFail(self):
        with self.assertRaises(TypeError, msg="type error should have been raised if an instructor was assigned as a ta"):
            CourseClass.assignTA(self, self.new_course, self.user_instructor)

    def test_AssignTAFail2(self):
        with self.assertRaises(TypeError, msg="type error should have been raised if a supervisor was assigned as a ta"):
            CourseClass.assignTA(self, self.new_course, self.user_instructor)

    def test_AssignInstructorNone(self):
        with self.assertRaises(TypeError, msg="type error should have been raised if no one was assigned"):
           CourseClass.assignTA(self, self.new_course, None)

    def test_AssignTABadCourse(self):
        with self.assertRaises(TypeError, msg="should raise typeerror if bad input"):
            CourseClass.assignTA(self, "course", self.user_TA)

    def test_AssignTANoCourse(self):
        with self.assertRaises(TypeError, msg="should raise typeerror if bad input"):
            CourseClass.assignTA(self, None, self.user_TA)


class TestCourseRemoveTA(TestCase):  # Void course.removeTA(course, TA)
    def setUp(self):
        self.address = "3400 N Maryland Avenue, Milwaukee, WI, 53211"
        self.password = "default_password"

        self.user_supervisor = User(email="jndoe@example.com", account_type=AccountType.SUPERVISOR, first_name="Jane", last_name="Doe", address=self.address, phone_number="9998887777", password=self.password)
        self.user_supervisor.save()

        self.user_instructor = User(email="jndoe@example.com", account_type=AccountType.INSTRUCTOR, first_name="Jake", last_name="Doe", address=self.address, phone_number="9998887777", password=self.password)
        self.user_instructor.save()

        self.user_TA = User(email="jndoe@example.com", account_type=AccountType.TA, first_name="Joe", last_name="Doe", address=self.address, phone_number="9998887777", password=self.password)
        self.user_TA.save()

        self.new_course = Course(name="Software Engineering", number=361)
        self.new_course.save()

    def test_RemoveTASuccess(self):
        TAToCourseObj = TAToCourse(course=self.new_course, ta=self.user_TA)
        TAToCourseObj.save()
        CourseClass.removeTA(self, self.new_course, self.user_TA)
        listOfObjects = TAToCourse.objects.filter(course=self.new_course)
        self.assertEqual(0, len(listOfObjects), "ta should be removed from course")

    def test_RemoveTANone(self):
        with self.assertRaises(RuntimeError, msg="remove ta should raise runtime error if there is no ta to remove"):
            CourseClass.removeTA(self, self.new_course, self.user_TA)

    def test_RemoveTABadTA(self):
        self.assertRaises(TypeError, CourseClass.removeTA, self, self.new_course, "TA", msg="should raise typeerror if bad input")

    def test_RemoveTANoTA(self):
        self.assertRaises(TypeError, CourseClass.removeTA, self, self.new_course, None, msg="should raise typeerror if bad input")

    def test_RemoveTABadCourse(self):
        self.assertRaises(TypeError, CourseClass.removeTA, self, "course", self.user_TA, msg="should raise typeerror if bad input")

    def test_RemoveTANoCourse(self):
        self.assertRaises(TypeError, CourseClass.removeTA, self, None, self.user_TA, msg="should raise typeerror if bad input")


class TestGetInstructor(TestCase):   #User course.getInstructor(course)
    def setUp(self):
        self.address = "3400 N Maryland Avenue, Milwaukee, WI, 53211"
        self.password = "default_password"

        self.user_instructor = User(email="jndoe@example.com", account_type=AccountType.INSTRUCTOR, first_name="Jake", last_name="Doe", address=self.address, phone_number="9998887777", password=self.password)
        self.user_instructor.save()

        self.new_course = Course(name="Software Engineering", number=361)
        self.new_course.save()

    def test_GetInstructorSuccess(self):
        self.new_course.instructor = self.user_instructor
        self.assertEqual(CourseClass.getInstructor(self, self.new_course), self.user_instructor, "get instructor should return the instructor for the course")

    def test_GetInstructorNone(self):
        self.assertEqual(CourseClass.getInstructor(self, self.new_course), None, "get instructor should return none if the course does not have an instructor")

    def test_GetInstructorBadCourse(self):
        self.assertRaises(TypeError, CourseClass.getInstructor, self, "course", msg="should raise typeerror if bad input")

    def test_GetInstructorNoCourse(self):
        self.assertRaises(TypeError, CourseClass.getInstructor, self, None, msg="should raise typeerror if bad input")


class TestGetTA(TestCase):  # User course.getTA(course)
    def setUp(self):
        self.address = "3400 N Maryland Avenue, Milwaukee, WI, 53211"
        self.password = "default_password"

        self.user_TA = User(email="jndoe@example.com", account_type=AccountType.TA, first_name="Jake", last_name="Doe", address=self.address, phone_number="9998887777", password=self.password)
        self.user_TA.save()

        self.user_TA2 = User(email="jndoe@example.com", account_type=AccountType.TA, first_name="Joe", last_name="Doe", address=self.address, phone_number="9998887777", password=self.password)
        self.user_TA2.save()

        self.new_course = Course(name="Software Engineering", number=361)
        self.new_course.save()

    def test_GetTASuccess(self):
        TAToCourseObj = TAToCourse(course=self.new_course, ta=self.user_TA)
        TAToCourseObj.save()
        list = [self.user_TA]
        self.assertEqual(CourseClass.getTA(self, self.new_course), list, "get ta should return the ta for the course")

    def test_GetTAMultiple(self):
        TAToCourseObj = TAToCourse(course=self.new_course, ta=self.user_TA)
        TAToCourseObj.save()
        TAToCourseObj2 = TAToCourse(course=self.new_course, ta=self.user_TA2)
        TAToCourseObj2.save()
        self.assertEqual(CourseClass.getTA(self, self.new_course), list((self.user_TA, self.user_TA2)), "get ta should return the tas for the course")

    def test_GetTANone(self):
        self.assertEqual(CourseClass.getTA(self, self.new_course), None, "get ta should return none if the course does not have an ta")

    def test_GetTABadInput(self):
        self.assertRaises(TypeError, CourseClass.getTA, self, "course", msg="should raise error on bad input")

    def test_GetTANoInput(self):
        self.assertRaises(TypeError, CourseClass.getTA, self, None, msg="should raise error on bad input")
