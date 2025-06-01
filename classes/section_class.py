from enum import Enum

from typing import List

from django.core.exceptions import ObjectDoesNotExist

from ProjectApp.models import Section, User
from classes.abstract.databaseable_interface import DatabaseObj
from classes.abstract.user_assignable_interface import SingleUserAssignable
from classes.new_user_class import AccountType, NewUserClass


# Section class, written by Wyatt K.
# Represents a memory-resident Section and has methods
# to convert between this and Models

class SectionType(Enum):
    LECTURE = "LECTURE"
    LAB = "LAB"
    DISCUSSION = "DISCUSSION"

    def __init__(self, db_alias: str):
        self.db_alias = db_alias


class SectionClass(SingleUserAssignable, DatabaseObj):
    VALID_USER_ACCOUNT_TYPES: List[AccountType] = [AccountType.TA, AccountType.INSTRUCTOR]

    section_type: SectionType
    user: NewUserClass
    number: int
    location: str
    start_time: str
    end_time: str
    week_days: str

    def __init__(self, section_type: SectionType, number: int, location: str,
                 start_time: str, end_time: str, week_days: str):

        # Set all fields with setters to reuse type checking
        self.set_section_type(section_type)
        self.set_number(number)
        self.set_location(location)
        self.set_start_time(start_time)
        self.set_end_time(end_time)
        self.set_week_days(week_days)

        # noinspection PyTypeChecker
        self.user = None

    def set_section_type(self, section_type: SectionType):

        if section_type is None:
            raise TypeError("section_type cannot be None.")

        if not isinstance(section_type, SectionType):
            raise TypeError("section_type must be of type SectionType.")

        self.section_type = section_type

    def get_section_type(self) -> SectionType:
        return self.section_type

    def assign_user(self, user: NewUserClass):
        if user is None:
            raise TypeError("user cannot be None.")

        if not isinstance(user, NewUserClass):
            raise TypeError("user must be of type UserClass")

        if not self.VALID_USER_ACCOUNT_TYPES.__contains__(user.account_type):
            raise TypeError("Invalid user role: " + str(user.account_type))

        self.user = user

    # noinspection PyTypeChecker
    def remove_user(self):

        if self.user is None:
            raise RuntimeError("Cannot remove user from Section as it is already None.")

        self.user = None

    def get_user(self) -> NewUserClass:
        return self.user

    def set_number(self, number: int):

        if number is None:
            raise TypeError("number cannot be None.")

        if not isinstance(number, int):
            raise TypeError("number must be of type int.")

        if number < 0:
            raise RuntimeError("number cannot be negative.")

        self.number = number

    def get_number(self) -> int:
        return self.number

    def set_location(self, location: str):

        if location is None:
            raise TypeError("location cannot be None.")

        if not isinstance(location, str):
            raise TypeError("location must be of type str.")

        if not location:
            raise RuntimeError("location string cannot be empty.")

        self.location = location

    def get_location(self) -> str:
        return self.location

    def set_start_time(self, start_time: str):

        if start_time is None:
            raise TypeError("start_time cannot be None.")

        if not isinstance(start_time, str):
            raise TypeError("start_time must be of type SectionType.")

        if not start_time:
            raise RuntimeError("start_time string cannot be empty.")

        self.start_time = start_time
        pass

    def get_start_time(self) -> str:
        return self.start_time

    def set_end_time(self, end_time: str):

        if end_time is None:
            raise TypeError("end_time cannot be None.")

        if not isinstance(end_time, str):
            raise TypeError("end_time must be of type SectionType.")

        if not end_time:
            raise RuntimeError("end_time string cannot be empty.")

        self.end_time = end_time

    def get_end_time(self) -> str:
        return self.end_time

    def set_week_days(self, week_days: str):

        if week_days is None:
            raise TypeError("week_days cannot be None.")

        if not isinstance(week_days, str):
            raise TypeError("week_days must be of type str.")

        self.week_days = week_days

    def get_week_days(self) -> str:
        return self.week_days

    # Private method
    # Does not need unit testing
    def __internal_save(self, model_section: Section):

        # Create ModelSection and populate its fields
        model_section.number = self.number
        model_section.section_type = self.section_type.db_alias
        model_section.location = self.location
        model_section.start_time = self.start_time
        model_section.end_time = self.end_time
        model_section.week_days = self.week_days

        # If user exists, try to set it
        if self.user is not None:
            try:
                model_user = User.objects.get(email=self.user.email)
                model_section.user = model_user
            except ObjectDoesNotExist:
                raise RuntimeError("User does not exist. Must save it first.")
        else:
            model_section.user = None

        # Save to db
        model_section.save()

    # Save using given Model Section, reuse the ID/overwrite
    # error if model_section does not already exist
    def overwrite(self, previous_section_info: Section):
        if previous_section_info is None:
            raise TypeError("previous_section_info cannot be None.")

        if not isinstance(previous_section_info, Section):
            raise TypeError("previous_section_info must be of type Section.")

        try:
            model_section = Section.objects.get(id=previous_section_info.id)
        except ObjectDoesNotExist:
            raise RuntimeError("Given Model Section has not already been saved to database.")

        self.__internal_save(model_section)

    # Return the Section's ID
    # create a new Section model each time this is called (if saved multiple times, don't try to combine)
    # Probably call save() for code reuse
    def save_new(self):
        model_section: Section = Section()
        self.__internal_save(model_section)

    @staticmethod
    def delete(section_id: int):
        if not isinstance(section_id, int):
            raise TypeError("section_id must be an int. Did you pass None?")

        try:
            model_section = Section.objects.get(id=section_id)
        except ObjectDoesNotExist:
            raise RuntimeError("No section with the given id could be found")

        try:
            model_section.delete()
        except:
            return False

        return True

    @staticmethod
    def from_model(model_section: Section):
        if model_section is None:
            raise TypeError("model_section cannot be None.")

        if not isinstance(model_section, Section):
            raise TypeError("model_section must be of type ModelSection.")

        # Prepare arguments from ModelSection
        section_type = SectionType[model_section.section_type.upper()]
        number = int(model_section.number)
        location = model_section.location
        start_time = model_section.start_time
        end_time = model_section.end_time
        week_days = model_section.week_days

        # Construct Section
        section = SectionClass(section_type, number, location, start_time, end_time, week_days)

        # Load User
        model_user: User = model_section.user

        # If it exists, create a new UserClass and assign it
        if model_user is not None:
            u_email = model_user.email
            u_account_type = AccountType[model_user.account_type.upper()]
            u_first_name = model_user.first_name
            u_last_name = model_user.last_name

            user: NewUserClass = NewUserClass(u_email, u_account_type, u_first_name, u_last_name)

            section.assign_user(user)

        return section
