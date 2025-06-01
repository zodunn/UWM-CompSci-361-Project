from typing import List
from django.core.exceptions import ObjectDoesNotExist
from ProjectApp.models import User, Section, TAToCourse, Course
import enum

from classes.abstract.databaseable_interface import DatabaseObjInternalKey


class Category(enum.Enum):
    phone = 1
    email = 2
    address = 3
    skills = 4


class PersonalInfoCategory(enum.Enum):
    first_name = "first_name"
    last_name = "last_name"
    email = "email"


class AccountType(enum.Enum):
    TA = "TA"
    INSTRUCTOR = "Instructor"
    SUPERVISOR = "Supervisor"

    def __init__(self, db_alias: str):
        self.db_alias = db_alias


class NewUserClass(DatabaseObjInternalKey):
    email: str
    account_type: AccountType
    first_name: str
    last_name: str
    password: str
    phone_number: str
    address: str
    office_hours_days: str
    office_hours_times: str
    office_hours_room: str
    skills: str

    # noinspection PyTypeChecker
    def __init__(self, email: str, account_type: AccountType, first_name: str, last_name: str):
        if not isinstance(email, str):
            raise TypeError("email must be of type String")

        if not isinstance(account_type, AccountType):
            raise TypeError("account_type must be of type AccountType")

        self.email = email
        self.account_type = account_type

        self.set_first_name(first_name)
        self.set_last_name(last_name)
        self.set_password("default")
        self.phone_number = ""
        self.address = None
        self.office_hours_days = None
        self.office_hours_times = None
        self.office_hours_room = None
        self.skills = None

    def get_email(self) -> str:
        return self.email

    def get_account_type(self) -> AccountType:
        return self.account_type

    def set_first_name(self, new_first_name: str):
        if not isinstance(new_first_name, str):
            raise TypeError("new_first_name must be of type str")

        if not new_first_name:
            raise RuntimeError("new_first_name cannot be empty")

        self.first_name = new_first_name

    def get_first_name(self) -> str:
        return self.first_name

    def set_last_name(self, new_last_name: str):
        if not isinstance(new_last_name, str):
            raise TypeError("new_last_name must be of type str")

        if not new_last_name:
            raise RuntimeError("new_last_name cannot be empty")

        self.last_name = new_last_name

    def get_last_name(self) -> str:
        return self.last_name

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def set_password(self, new_password: str):
        if not isinstance(new_password, str):
            raise TypeError("new_password must be of type str")

        if not new_password:
            raise RuntimeError("new_password cannot be empty")

        self.password = new_password

    def get_password(self) -> str:
        return self.password

    # None allowed
    def set_phone_number(self, new_phone_number: str):
        if not isinstance(new_phone_number, str):
            raise TypeError("new_phone_number must be of type str")

        if not new_phone_number:
            raise RuntimeError("new_phone_number cannot be empty")

        self.phone_number = new_phone_number

    def get_phone_number(self) -> str:
        return self.phone_number

    def set_address(self, new_address: str):
        if not isinstance(new_address, str):
            raise TypeError("new_address must be of type str")

        if not new_address:
            raise RuntimeError("new_address cannot be empty")

        self.address = new_address

    def get_address(self) -> str:
        return self.address

    # noinspection PyTypeChecker
    def remove_address(self):
        self.address = None

    def set_office_hours_days(self, new_office_days: str):
        if not isinstance(new_office_days, str):
            raise TypeError("new_office_days must be of type str")

        self.office_hours_days = new_office_days
        if new_office_days:
            self.save()

    def set_office_hours_room(self, new_office_room: str):
        if not isinstance(new_office_room, str):
            raise TypeError("new_office_room must be of type str")

        self.office_hours_room = new_office_room
        if new_office_room:
            self.save()

    def set_office_hours_times(self, new_office_times: str):
        if not isinstance(new_office_times, str):
            raise TypeError("new_office_times must be of type str")

        self.office_hours_times = new_office_times
        if new_office_times:
            self.save()

    def remove_office_hours_days(self):
        self.office_hours_days = None

    def remove_office_hours_room(self):
        self.office_hours_room = None

    def remove_office_hours_times(self):
        self.office_hours_times = None

    # Order: days, room, time
    def get_office_hours_data(self) -> List[str]:
        return [self.office_hours_days, self.office_hours_room, self.office_hours_times]

    def getPrivAccountData(self, caller: User, user: User):
        if not isinstance(user, User):
            raise TypeError

        if not caller == user and not caller.account_type == AccountType.SUPERVISOR:
            raise RuntimeError("Insufficient permissions to get private account data")

        data_list = [user.first_name, user.last_name, user.email, user.account_type, user.address, user.phone_number]
        return data_list

    def getOfficeHoursData(self, user: User):
        if not isinstance(user, User):
            raise TypeError

        return [user.office_hours_days, user.office_hours_room, user.office_hours_times]

    def getSkills(self, user):
        if not isinstance(user, User):
            raise TypeError
        return user.skills

    def addSkill(self, user, skill):
        if not isinstance(user, User) or not isinstance(skill, str):
            raise TypeError
        user.skills = skill

    def addContactInfo(self, user, category, visibility, input):
        if not isinstance(input, str):
            raise TypeError
        if not isinstance(user, User):
            raise TypeError
        if category.name == "phone":
            if input == "":
                category.phone = ""
            else:
                if not len(input) == 10:
                    raise RuntimeError
                if not input.isnumeric():
                    raise RuntimeError
                user.phone_number = input
            user.save()
        if category.name == "email":
            raise RuntimeError
        if category.name == "address":
            if input == "":
                user.address = ""
            else:
                holder = input
                input = input.split(",")
                if not len(input) == 4:
                    raise RuntimeError
                user.address = holder
            user.save()

    def getContactInfo(self, user):
        if not isinstance(user, User):
            raise TypeError
        return [user.phone_number, user.email, user.address]

    @staticmethod
    def logIn(Username, Password):
        if not isinstance(Username, str) or not isinstance(Password, str):
            raise TypeError

        try:
            user = User.objects.get(email=Username)

            # Check if it's a bad password
            if user.password != Password:
                return False

        # Exception raised if user does not exist
        except ObjectDoesNotExist:
            return False

        return True

    def setUserInfo(self, user, category, value):
        if not isinstance(user, User) or not isinstance(value, str):
            raise TypeError
        if isinstance(category, int) or isinstance(category, float) or isinstance(category, bool):
            raise TypeError

        if not value:
            raise RuntimeError("Cannot pass empty value")

        if category == PersonalInfoCategory.first_name:
            user.first_name = value
        elif category == PersonalInfoCategory.last_name:
            user.last_name = value
        elif category == PersonalInfoCategory.email:
            user.email = value
        else:
            raise TypeError("Invalid PersonalInfoCategory: " + str(category))

    def deleteAccount(self, userDelete, supervisor):
        if not isinstance(userDelete, User) or not isinstance(supervisor, User):
            raise TypeError
        if userDelete.account_type == 'TA':
            for course in TAToCourse.objects.all():
                if course.ta == userDelete:
                    raise RuntimeError
        if userDelete.account_type == 'Instructor':
            for course in Course.objects.all():
                if course.instructor == userDelete:
                    raise RuntimeError
        try:
            User.objects.get(email=userDelete.email).delete()
        except Exception as e:
            a = e
            raise RuntimeError

    def setPassword(self, user, newPass, oldPass):
        if newPass == "" or newPass is oldPass or not user.password == oldPass:
            raise RuntimeError
        if not isinstance(newPass, str) or not isinstance(oldPass, str):
            raise TypeError
        user.password = newPass
        user.save()

    def getUserInfo(self, user, category):
        if user == None or category == None or not isinstance(user, User) or not isinstance(category.name, str):
            raise TypeError
        if category.name == 'first_name':
            return user.first_name
        if category.name == 'last_name':
            return user.last_name
        if category.name == 'email':
            return user.email

    def getTAs(self, course):
        if not isinstance(course, Course):
            raise TypeError
        if course is None:
            raise TypeError("course cannot be None")
        taToCourse = TAToCourse.objects.all()
        listy = []
        for taToCourse in taToCourse:
            if taToCourse.course == course:
                listy.append(taToCourse.ta)
        return listy

    def getCourse(self, user):
        if not isinstance(user, User) or user == None:
            raise TypeError
        all_courses = Course.objects.all()
        listy = []
        for course in all_courses:
            if course.instructor == user:
                listy.append(course)
        return listy

    def getCourseTA(self, user):
        if not isinstance(user, User) or user == None:
            raise TypeError
        taToCourse = TAToCourse.objects.all()
        listy = []
        for ta_course_link in taToCourse:
            if ta_course_link.ta == user:
                listy.append(ta_course_link.course)
        return listy

    def getSection(self, user):
        if not isinstance(user, User):
            raise TypeError
        if user is None:
            raise TypeError("user cannot be None.")
        all_sections = Section.objects.all()
        listy = []
        for section in all_sections:
            if section.user == user:
                listy.append(section)
        return listy

    def save(self):

        try:
            model_user: User = User.objects.get(email=self.email)
        except ObjectDoesNotExist:
            model_user: User = User()

        model_user.email = self.email
        model_user.account_type = self.account_type.db_alias
        model_user.first_name = self.first_name
        model_user.last_name = self.last_name
        model_user.password = self.password
        model_user.phone_number = NewUserClass.none_to_empty_string(self.phone_number)
        model_user.address = NewUserClass.none_to_empty_string(self.address)
        model_user.office_hours_days = NewUserClass.none_to_empty_string(self.office_hours_days)
        model_user.office_hours_times = NewUserClass.none_to_empty_string(self.office_hours_times)
        model_user.office_hours_room = NewUserClass.none_to_empty_string(self.office_hours_room)
        model_user.skills = NewUserClass.none_to_empty_string(self.skills)

        model_user.save()

    @staticmethod
    def from_model(model_user: User):
        if not isinstance(model_user, User):
            raise TypeError("model_user most be of type User")

        # Prepare arguments from ModelUser
        account_type = AccountType[model_user.account_type.upper()]
        email = model_user.email
        first_name = model_user.first_name
        last_name = model_user.last_name
        password = model_user.password
        phone_number = model_user.phone_number
        address = model_user.address
        office_days = model_user.office_hours_days
        office_times = model_user.office_hours_times
        office_room = model_user.office_hours_room
        skills = model_user.skills

        # Construct User
        user = NewUserClass(email, account_type, first_name, last_name)
        user.password = password

        # Set optional stuff, or None if the string was empty
        user.address = NewUserClass.none_to_empty_string(address)
        user.phone_number = NewUserClass.none_to_empty_string(phone_number)
        user.office_hours_days = NewUserClass.none_to_empty_string(office_days)
        user.office_hours_times = NewUserClass.none_to_empty_string(office_times)
        user.office_hours_room = NewUserClass.none_to_empty_string(office_room)

        user.skills = NewUserClass.none_to_empty_string(skills)

        return user

    @staticmethod
    def empty_string_to_none(in_string: str):
        if in_string:
            return in_string
        else:
            return None

    @staticmethod
    def none_to_empty_string(in_string: str):
        if in_string is None:
            return ""
        else:
            return in_string
