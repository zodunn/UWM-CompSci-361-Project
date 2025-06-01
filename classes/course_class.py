from django.core.exceptions import ObjectDoesNotExist

from ProjectApp.models import Course, SectionToCourse, Section, User, TAToCourse
from classes.new_user_class import AccountType


class CourseClass(object):
    def __init__(self, courseName, courseNumber):
        self.courseName = courseName
        self.courseNumber = courseNumber

    def addSection(self, course, section):
        if not isinstance(course, Course) or not isinstance(section, Section):
            raise TypeError

        validCourse = True
        validSection = True
        notAlreadyInCourse = False

        try:
            Course.objects.get(number=course.number)
        except ObjectDoesNotExist:
            validCourse = False

        try:
            Section.objects.get(number=section.number)
        except ObjectDoesNotExist:
            validSection = False

        try:
            SectionToCourse.objects.get(section=section)
        except ObjectDoesNotExist:
            notAlreadyInCourse = True

        if not validCourse or not validSection:
            return TypeError

        if notAlreadyInCourse:
            sectionTOCourseObj = SectionToCourse(course=course, section=section)
            sectionTOCourseObj.save()
        else:
            raise RuntimeError

    def assignInstructor(self, course, instructor):
        if not isinstance(course, Course):
            raise TypeError("Course must be of type Course")

        if not isinstance(instructor, User):
            raise TypeError("Instructor must be of type User")

        if not (instructor.account_type == AccountType.INSTRUCTOR or instructor.account_type == "AccountType.INSTRUCTOR"
                or instructor.account_type == "INSTRUCTOR" or instructor.account_type == "Instructor"):
            raise TypeError("Instructor must be of AccountType INSTRUCTOR")
            
        course.instructor = instructor

    def assignTA(self, course, TA):
        if not isinstance(course, Course):
            raise TypeError("Course must be of type Course")

        if not isinstance(TA, User):
            raise TypeError("TA must be of type User")

        print(TA.account_type)

        if not (TA.account_type == AccountType.TA or TA.account_type == "AccountType.TA"
                or TA.account_type == "TA" or TA.account_type == "ta"):
            raise TypeError("TA must be of AccountType TA")

        TAToCourse.objects.create(course=course, ta=TA)

    def getName(self, course):
        if not isinstance(course, Course):
            raise TypeError
        return course.name

    def getNumber(self, course):
        if not isinstance(course, Course):
            raise TypeError
        return course.number

    def getSections(self, course):
        listy = []
        for section in list(SectionToCourse.objects.filter(course=course)):
            listy.append(section.section)
        return listy

    def removeInstructor(self, course):
        if not isinstance(course, Course):
            raise TypeError
        if course.instructor == None:
            raise RuntimeError
        course.instructor = None

    def removeTA(self, course, TA):
        if not isinstance(course, Course) or not isinstance(TA, User):
            raise TypeError
        try:
            tatocourse = TAToCourse.objects.filter(ta=TA).get(course=course)
            tatocourse.delete()
        except:
            raise RuntimeError

    def setName(self, course, name):
        if not isinstance(course, Course) or not isinstance(name, str):
            raise TypeError
        if not name.isalpha:
            raise RuntimeError
        course.name = name

    def getInstructor(self, course):
        if not isinstance(course, Course):
            raise TypeError
        return course.instructor

    def getTA(self, course):
        if not isinstance(course, Course):
            raise TypeError
        listy = []
        for obj in list(TAToCourse.objects.filter(course=course)):
            listy.append(obj.ta)
        if len(listy) == 0:
            return None
        return listy
