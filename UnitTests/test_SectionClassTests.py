from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from ProjectApp.models import Section, User
from classes.section_class import SectionClass, SectionType
from classes.new_user_class import NewUserClass, AccountType



# SectionTests class, written by Wyatt K.
# Tests for the Section class.

class TestSectionConstructor(TestCase):
    s_section = SectionType.LECTURE
    s_num = 0
    s_loc = "location"
    s_start = "8:00"
    s_end = "8:30"
    s_days = "MT"

    def testValid(self):
        section = SectionClass(self.s_section, self.s_num, self.s_loc, self.s_start, self.s_end, self.s_days)
        self.assertEquals(self.s_section, section.get_section_type(), msg="Incorrect SectionType after constructor")
        self.assertEquals(self.s_num, section.get_number(), msg="Incorrect Section number after constructor")
        self.assertEquals(self.s_loc, section.get_location(), msg="Incorrect Section Location after constructor")
        self.assertEquals(self.s_start, section.get_start_time(),
                          msg="Incorrect Section start time after constructor")
        self.assertEquals(self.s_end, section.get_end_time(), msg="Incorrect Section end time after constructor")
        self.assertEquals(self.s_days, section.get_week_days(), msg="Incorrect Section day after constructor")

        self.assertEquals(None, section.get_user(), msg="Section has a user after constructor")

    # noinspection PyTypeChecker
    def testNoneTypes(self):
        def_sec = self.s_section
        def_num = self.s_num
        def_loc = self.s_loc
        def_start = self.s_start
        def_end = self.s_end
        def_day = self.s_days

        with self.assertRaises(TypeError, msg="Did not raise TypeError for None section"):
            SectionClass(None, def_num, def_loc, def_start, def_end, def_day)

        with self.assertRaises(TypeError, msg="Did not raise TypeError for None number"):
            SectionClass(def_sec, None, def_loc, def_start, def_end, def_day)

        with self.assertRaises(TypeError, msg="Did not raise TypeError for None location"):
            SectionClass(def_sec, def_num, None, def_start, def_end, def_day)

        with self.assertRaises(TypeError, msg="Did not raise TypeError for None start time"):
            SectionClass(def_sec, def_num, def_loc, None, def_end, def_day)

        with self.assertRaises(TypeError, msg="Did not raise TypeError for None end time"):
            SectionClass(def_sec, def_num, def_loc, def_start, None, def_day)

        with self.assertRaises(TypeError, msg="Did not raise TypeError for None day"):
            SectionClass(def_sec, def_num, def_loc, def_start, def_end, None)

    # noinspection PyTypeChecker
    def testWrongType(self):
        def_sec = self.s_section
        def_num = self.s_num
        def_loc = self.s_loc
        def_start = self.s_start
        def_end = self.s_end
        def_day = self.s_days

        # Boolean is never used as an arg
        def_incorrect_type = ["this", "is", "invalid"]

        with self.assertRaises(TypeError, msg="Did not raise TypeError for incorrect-type section"):
            SectionClass(def_incorrect_type, def_num, def_loc, def_start, def_end, def_day)

        with self.assertRaises(TypeError, msg="Did not raise TypeError for incorrect-type number"):
            SectionClass(def_sec, def_incorrect_type, def_loc, def_start, def_end, def_day)

        with self.assertRaises(TypeError, msg="Did not raise TypeError for incorrect-type location"):
            SectionClass(def_sec, def_num, def_incorrect_type, def_start, def_end, def_day)

        with self.assertRaises(TypeError, msg="Did not raise TypeError for incorrect-type start time"):
            SectionClass(def_sec, def_num, def_loc, def_incorrect_type, def_end, def_day)

        with self.assertRaises(TypeError, msg="Did not raise TypeError for incorrect-type end time"):
            SectionClass(def_sec, def_num, def_loc, def_start, def_incorrect_type, def_day)

        with self.assertRaises(TypeError, msg="Did not raise TypeError for incorrect-type day"):
            SectionClass(def_sec, def_num, def_loc, def_start, def_end, def_incorrect_type)


# noinspection DuplicatedCode
class TestSectionAssignAndGetUser(TestCase):
    def setUp(self):
        test_u_email = "someone@example.com"
        test_u_account_type = AccountType.TA
        test_u_first_name = "Dink"
        test_u_last_name = "Smallwood"

        self.user = NewUserClass(test_u_email, test_u_account_type, test_u_first_name, test_u_last_name)

        test_su_email = "someone2@example.com"
        test_su_account_type = AccountType.SUPERVISOR
        test_su_first_name = "Dink2"
        test_su_last_name = "Smallwood2"

        self.supervisor = NewUserClass(test_su_email, test_su_account_type, test_su_first_name, test_su_last_name)

        test_s_type = SectionType.LAB
        test_s_number = 401
        test_s_location = "Test"
        test_s_start_time = "8:00"
        test_s_end_time = "8:30"
        test_s_day = "M"

        self.section = SectionClass(test_s_type, test_s_number, test_s_location, test_s_start_time, test_s_end_time,
                                    test_s_day)

    def testValid(self):
        self.section.assign_user(self.user)
        self.assertEqual(self.user, self.section.get_user(), msg="Section wrong User after assign_user")

    # noinspection PyTypeChecker
    def testNoneFromUser(self):
        self.section.assign_user(self.user)

        with self.assertRaises(TypeError, msg="assign_user Did not raise TypeError for None input"):
            self.section.assign_user(None)

        self.assertEqual(self.user, self.section.get_user(), msg="assign_user assigned User for None input")

    # noinspection PyTypeChecker
    def testNoneFromNone(self):
        with self.assertRaises(TypeError, msg="assign_user Did not raise TypeError for None input"):
            self.section.assign_user(None)

    # noinspection PyTypeChecker
    def testInvalidType(self):
        str_var = "potato"

        with self.assertRaises(TypeError, msg="assign_user Did not raise TypeError for invalid input type"):
            self.section.assign_user(str_var)

        self.assertNotEqual(self.section.get_user(), str_var, "assign_user set user for invalid input type")

    def testInvalidRole(self):
        with self.assertRaises(TypeError, msg="assign_user Did not raise TypeError for invalid user role (supervisor)"):
            self.section.assign_user(self.supervisor)

        self.assertNotEqual(self.section.get_user(), self.supervisor,
                            "assign_user set user for invalid user role (supervisor)")


class TestSectionRemoveUser(TestCase):
    def setUp(self):
        test_u_email = "someone@example.com"
        test_u_account_type = AccountType.TA
        test_u_first_name = "Dink"
        test_u_last_name = "Smallwood"

        self.user = NewUserClass(test_u_email, test_u_account_type, test_u_first_name, test_u_last_name)

        test_s_type = SectionType.LAB
        test_s_number = 401
        test_s_location = "Test"
        test_s_start_time = "8:00"
        test_s_end_time = "8:30"
        test_s_day = "M"

        self.section = SectionClass(test_s_type, test_s_number, test_s_location, test_s_start_time, test_s_end_time,
                                    test_s_day)

    def testSuccess(self):
        self.section.assign_user(self.user)
        self.section.remove_user()
        self.assertIsNone(self.section.get_user(), "remove_user did not remove the user.")

    def testRemoveAlreadyEmpty(self):
        with self.assertRaises(RuntimeError, msg="Remove User did not error when removing user when it had none."):
            self.section.remove_user()


class TestSectionSetAndGetNumber(TestCase):
    test_number = 401
    test_number_2 = 501
    test_number_negative = -1
    test_in_str = "test"

    def setUp(self):
        test_s_type = SectionType.LAB
        test_s_location = "Test"
        test_s_start_time = "8:00"
        test_s_end_time = "8:30"
        test_s_day = "M"

        self.section = SectionClass(test_s_type, self.test_number, test_s_location, test_s_start_time, test_s_end_time,
                                    test_s_day)

    def testGetNumber(self):
        self.assertEqual(self.section.get_number(), self.test_number, msg="get_number returned incorrect number")

    def testSetNumberValid(self):
        self.section.set_number(self.test_number_2)
        self.assertEqual(self.section.get_number(), self.test_number_2, msg="set_number did not set number correctly")

    def testSetNumberNegative(self):
        with self.assertRaises(RuntimeError, msg="Negative number did not raise RuntimeError for set_number"):
            self.section.set_number(self.test_number_negative)

    # noinspection PyTypeChecker
    def testSetNumberNone(self):
        with self.assertRaises(TypeError, msg="set_number(None) did not raise TypeError"):
            self.section.set_number(None)

    # noinspection PyTypeChecker
    def testSetNumberWrongType(self):
        with self.assertRaises(TypeError, msg="set_number(wrong type) did not raise TypeError"):
            self.section.set_number(self.test_in_str)


class TestSectionSetAndGetLocation(TestCase):
    test_input_default = "EMS E180"
    test_input_alt = "Sandburg 403"
    test_input_empty = ""
    test_input_int = 5

    def setUp(self):
        test_s_type = SectionType.LAB
        test_s_number = 401
        test_s_start_time = "8:00"
        test_s_end_time = "8:30"
        test_s_day = "M"

        self.section = SectionClass(test_s_type, test_s_number, self.test_input_default, test_s_start_time,
                                    test_s_end_time,
                                    test_s_day)

    def testGetLocation(self):
        self.assertEqual(self.section.get_location(), self.test_input_default,
                         msg="get_location returned incorrect location")

    def testSetLocationValid(self):
        self.section.set_location(self.test_input_alt)
        self.assertEqual(self.section.get_location(), self.test_input_alt,
                         msg="set_location did not set location correctly")

    def testSetLocationEmpty(self):
        with self.assertRaises(RuntimeError, msg="Empty string did not raise RuntimeError for set_location"):
            self.section.set_location(self.test_input_empty)

    # noinspection PyTypeChecker
    def testSetLocationNone(self):
        with self.assertRaises(TypeError, msg="set_location(None) did not raise TypeError"):
            self.section.set_location(None)

    # noinspection PyTypeChecker
    def testSetLocationWrongType(self):
        with self.assertRaises(TypeError, msg="set_location(wrong type) did not raise TypeError"):
            self.section.set_location(self.test_input_int)


class TestSectionSetAndGetStartTime(TestCase):
    test_input_default = "8:00"
    test_input_alt = "14:30"
    test_input_empty = ""
    test_input_wrong_type = 3

    def setUp(self):
        test_s_type = SectionType.LAB
        test_s_number = 401
        test_s_location = "Test"
        test_s_end_time = "8:30"
        test_s_day = "M"

        self.section = SectionClass(test_s_type, test_s_number, test_s_location, self.test_input_default,
                                    test_s_end_time, test_s_day)

    def testGetStartTime(self):
        self.assertEqual(self.section.get_start_time(), self.test_input_default,
                         msg="get_start_time returned incorrect time")

    def testSetStartTimeValid(self):
        self.section.set_start_time(self.test_input_alt)
        self.assertEqual(self.section.get_start_time(), self.test_input_alt,
                         msg="set_start_time did not set time correctly")

    # noinspection PyTypeChecker
    def testSetStartTimeEmpty(self):
        with self.assertRaises(RuntimeError, msg="set_start_time(empty) did not raise RuntimeError"):
            self.section.set_start_time(self.test_input_empty)

    # noinspection PyTypeChecker
    def testSetStartTimeNone(self):
        with self.assertRaises(TypeError, msg="set_start_time(None) did not raise TypeError"):
            self.section.set_start_time(None)

    # noinspection PyTypeChecker
    def testSetStartTimeWrongType(self):
        with self.assertRaises(TypeError, msg="set_start_time(wrong type) did not raise TypeError"):
            self.section.set_start_time(self.test_input_wrong_type)


class TestSectionSetAndGetEndTime(TestCase):
    test_input_default = "8:30"
    test_input_alt = "14:30"
    test_input_empty = ""
    test_input_wrong_type = 3

    def setUp(self):
        test_s_type = SectionType.LAB
        test_s_number = 401
        test_s_location = "Test"
        test_s_start_time = "8:00"
        test_s_day = "M"

        self.section = SectionClass(test_s_type, test_s_number, test_s_location, test_s_start_time,
                                    self.test_input_default, test_s_day)

    def testGetEndTime(self):
        self.assertEqual(self.section.get_end_time(), self.test_input_default,
                         msg="get_end_time returned incorrect time")

    def testSetEndTimeValid(self):
        self.section.set_end_time(self.test_input_alt)
        self.assertEqual(self.section.get_end_time(), self.test_input_alt,
                         msg="set_end_time did not set time correctly")

    # noinspection PyTypeChecker
    def testSetEndTimeEmpty(self):
        with self.assertRaises(RuntimeError, msg="set_end_time(empty) did not raise RuntimeError"):
            self.section.set_end_time(self.test_input_empty)

    # noinspection PyTypeChecker
    def testSetEndTimeNone(self):
        with self.assertRaises(TypeError, msg="set_end_time(None) did not raise TypeError"):
            self.section.set_end_time(None)

    # noinspection PyTypeChecker
    def testSetEndTimeWrongType(self):
        with self.assertRaises(TypeError, msg="set_end_time(wrong type) did not raise TypeError"):
            self.section.set_end_time(self.test_input_wrong_type)


class TestSectionSetAndGetWeekDay(TestCase):
    test_input_default = "M"
    test_input_alt = "R"
    test_input_int = 5

    def setUp(self):
        test_s_type = SectionType.LAB
        test_s_number = 401
        test_s_location = "Test"
        test_s_start_time = "8:00"
        test_s_end_time = "8:30"

        self.section = SectionClass(test_s_type, test_s_number, test_s_location, test_s_start_time,
                                    test_s_end_time, self.test_input_default)

    def testGetWeekDay(self):
        self.assertEqual(self.section.get_week_days(), self.test_input_default,
                         msg="get_week_day returned incorrect location")

    def testSetWeekDayValid(self):
        self.section.set_week_days(self.test_input_alt)
        self.assertEqual(self.section.get_week_days(), self.test_input_alt,
                         msg="set_week_day did not set location correctly")

    # noinspection PyTypeChecker
    def testSetWeekDayNone(self):
        with self.assertRaises(TypeError, msg="set_week_day(None) did not raise TypeError"):
            self.section.set_week_days(None)

    # noinspection PyTypeChecker
    def testSetWeekDayWrongType(self):
        with self.assertRaises(TypeError, msg="set_week_day(wrong type) did not raise TypeError"):
            self.section.set_week_days(self.test_input_int)


# noinspection DuplicatedCode
class TestSectionSaveNew(TestCase):
    test_u_email = "someone@example.com"
    test_u_account_type = AccountType.TA
    test_u_first_name = "Dink"
    test_u_last_name = "Smallwood"
    test_u_password = "password"
    test_u_phone = "999-999-9999"
    test_u_address = "123 Spooky Street"

    test_s_type = SectionType.LAB
    test_s_number = 401
    test_s_location = "Test"
    test_s_start_time = "8:00"
    test_s_end_time = "8:30"
    test_s_day = "M"


# noinspection DuplicatedCode
class TestSectionSaveNew(TestCase):
    test_u_email = "someone@example.com"
    test_u_account_type = AccountType.TA
    test_u_first_name = "Dink"
    test_u_last_name = "Smallwood"
    test_u_password = "password"
    test_u_phone = "999-999-9999"
    test_u_address = "123 Spooky Street"

    test_s_type = SectionType.LAB
    test_s_number = 401
    test_s_location = "Test"
    test_s_start_time = "8:00"
    test_s_end_time = "8:30"
    test_s_day = "M"

    def setUp(self):
        self.db_user = User()
        self.db_user.email = self.test_u_email
        self.db_user.account_type = self.test_u_account_type
        self.db_user.first_name = self.test_u_first_name
        self.db_user.last_name = self.test_u_last_name
        self.db_user.password = self.test_u_password
        self.db_user.phone_number = self.test_u_phone
        self.db_user.address = self.test_u_address

        self.db_section = Section()
        self.db_section.number = self.test_s_number
        self.db_section.section_type = self.test_s_type.db_alias
        self.db_section.location = self.test_s_location
        self.db_section.start_time = self.test_s_start_time
        self.db_section.end_time = self.test_s_end_time
        self.db_section.week_days = self.test_s_day

        self.user = NewUserClass(self.test_u_email, self.test_u_account_type, self.test_u_first_name,
                              self.test_u_last_name)

        self.section = SectionClass(self.test_s_type, self.test_s_number, self.test_s_location, self.test_s_start_time,
                                    self.test_s_end_time, self.test_s_day)

    # noinspection PyTypeChecker
    def testSaveUserNotSaved(self):

        # Validate user does not exist
        try:
            User.objects.get(email=self.db_user.email)
            raise RuntimeError("User cannot already be saved for this test.")
        except ObjectDoesNotExist:
            pass

        self.section.assign_user(self.user)

        with self.assertRaises(RuntimeError, msg="Overwrite did not raise an error when User was not already saved"):
            self.section.save_new()

    # noinspection PyTypeChecker
    def testSaveUserNotPreviouslySaved(self):
        self.section.assign_user(self.user)

        with self.assertRaises(RuntimeError, msg="Overwrite did not raise an error when User was not already saved"):
            self.section.save_new()

    def testSaveNewValidNoUser(self):
        self.section.save_new()

        model_section: Section = Section.objects.get(number=self.section.number)

        # This is purely to keep the line width down
        db_type = self.test_s_type.db_alias

        self.assertEqual(model_section.section_type, db_type, msg="Invalid Model SectionType after save")
        self.assertEqual(model_section.location, self.test_s_location, msg="Invalid Model Location after save")
        self.assertEqual(model_section.start_time, self.test_s_start_time, msg="Invalid Model Start Time after save")
        self.assertEqual(model_section.end_time, self.test_s_end_time, msg="Invalid Model End Time after save")
        self.assertEqual(model_section.week_days, self.test_s_day, msg="Invalid Model Weekday after save")
        self.assertIsNone(model_section.user, msg="Model User is not None after save with no User")

    def testSaveNewValidYesUser(self):
        self.db_user.save()
        self.section.assign_user(self.user)
        self.section.save_new()

        model_section: Section = Section.objects.get(number=self.section.number)

        # This is purely to keep the line width down
        db_type = self.test_s_type.db_alias

        self.assertEqual(model_section.section_type, db_type, msg="Invalid Model SectionType after save")
        self.assertEqual(model_section.location, self.test_s_location, msg="Invalid Model Location after save")
        self.assertEqual(model_section.start_time, self.test_s_start_time, msg="Invalid Model Start Time after save")
        self.assertEqual(model_section.end_time, self.test_s_end_time, msg="Invalid Model End Time after save")
        self.assertEqual(model_section.week_days, self.test_s_day, msg="Invalid Model Weekday after save")
        self.assertIsNotNone(model_section.user, msg="Model User is None after save with no User")

    def testSaveNewTwice(self):
        self.section.save_new()
        self.section.save_new()

        model_count: int = Section.objects.filter(number=self.section.number).count()

        self.assertEqual(2, model_count, msg="Invalid model_count for double save: expected 2")


# noinspection DuplicatedCode
class TestSectionOverwrite(TestCase):
    test_u_email = "someone@example.com"
    test_u_account_type = AccountType.TA
    test_u_first_name = "Dink"
    test_u_last_name = "Smallwood"
    test_u_password = "password"
    test_u_phone = "999-999-9999"
    test_u_address = "123 Spooky Street"

    test_s_type = SectionType.LAB
    test_s_number = 401
    test_s_location = "Test"
    test_s_start_time = "8:00"
    test_s_end_time = "8:30"
    test_s_day = "M"

    def setUp(self):
        self.db_user = User()
        self.db_user.email = self.test_u_email
        self.db_user.account_type = self.test_u_account_type
        self.db_user.first_name = self.test_u_first_name
        self.db_user.last_name = self.test_u_last_name
        self.db_user.password = self.test_u_password
        self.db_user.phone_number = self.test_u_phone
        self.db_user.address = self.test_u_address

        self.db_section = Section()
        self.db_section.number = self.test_s_number
        self.db_section.section_type = self.test_s_type.db_alias
        self.db_section.location = self.test_s_location
        self.db_section.start_time = self.test_s_start_time
        self.db_section.end_time = self.test_s_end_time
        self.db_section.week_days = self.test_s_day

        self.user = NewUserClass(self.test_u_email, self.test_u_account_type, self.test_u_first_name,
                              self.test_u_last_name)

        self.section = SectionClass(self.test_s_type, self.test_s_number, self.test_s_location, self.test_s_start_time,
                                    self.test_s_end_time, self.test_s_day)

    # noinspection PyTypeChecker
    def testOverwriteNone(self):
        with self.assertRaises(TypeError, msg="Overwrite did not raise error on none input"):
            self.section.overwrite(None)

    # noinspection PyTypeChecker
    def testOverwriteWrongType(self):
        with self.assertRaises(TypeError, msg="Overwrite did not raise error on wrong-type input"):
            self.section.overwrite(3)

    # noinspection PyTypeChecker
    def testOverwriteUserNotSaved(self):

        # Initial save
        self.db_section.save()

        # Validate database
        Section.objects.get(id=self.db_section.id)

        # Ensure that User has not been saved
        try:
            User.objects.get(email=self.db_user.email)
            raise RuntimeError("User cannot already be saved for this test")
        except ObjectDoesNotExist:
            pass

        self.section.assign_user(self.user)

        with self.assertRaises(RuntimeError, msg="Overwrite did not raise an error when User was not already saved"):
            self.section.overwrite(self.db_section)

    def testOverwriteNoUser(self):
        # Initial save
        self.db_section.save()

        Section.objects.get(id=self.db_section.id)

        # Definitions for changes
        new_type = SectionType.DISCUSSION
        new_location = "Potato Land"
        new_start_time = "10:00"
        new_end_time = "10:30"
        new_week_day = "M"

        # Set new values
        self.section.set_section_type(new_type)
        self.section.set_location(new_location)
        self.section.set_start_time(new_start_time)
        self.section.set_end_time(new_end_time)
        self.section.set_week_days(new_week_day)

        # Save again
        self.section.overwrite(self.db_section)

        # Get sect from DB
        model_section = Section.objects.get(id=self.db_section.id)

        self.assertEqual(model_section.section_type, new_type.db_alias, msg="Invalid Model SectionType after overwrite")
        self.assertEqual(model_section.location, new_location, msg="Invalid Model Location after overwrite")
        self.assertEqual(model_section.start_time, new_start_time, msg="Invalid Model Start Time after overwrite")
        self.assertEqual(model_section.end_time, new_end_time, msg="Invalid Model End Time after overwrite")
        self.assertEqual(model_section.week_days, new_week_day, msg="Invalid Model Weekday after overwrite")
        self.assertIsNone(model_section.user, msg="Model User is not None after overwrite with no User")

    def testOverwriteYesUser(self):
        # Initial save
        self.db_user.save()
        self.db_section.user = self.db_user
        self.db_section.save()

        User.objects.get(email=self.db_user.email)
        Section.objects.get(id=self.db_section.id)

        # Definitions for changes
        new_type = SectionType.DISCUSSION
        new_location = "Potato Land"
        new_start_time = "10:00"
        new_end_time = "10:30"
        new_week_day = "M"

        # Set new values
        self.section.set_section_type(new_type)
        self.section.set_location(new_location)
        self.section.set_start_time(new_start_time)
        self.section.set_end_time(new_end_time)
        self.section.set_week_days(new_week_day)
        self.section.assign_user(self.user)

        # Save again
        self.section.overwrite(self.db_section)

        # Get sect from DB
        model_section = Section.objects.get(id=self.db_section.id)

        self.assertEqual(model_section.section_type, new_type.db_alias, msg="Invalid Model SectionType after overwrite")
        self.assertEqual(model_section.location, new_location, msg="Invalid Model Location after overwrite")
        self.assertEqual(model_section.start_time, new_start_time, msg="Invalid Model Start Time after overwrite")
        self.assertEqual(model_section.end_time, new_end_time, msg="Invalid Model End Time after overwrite")
        self.assertEqual(model_section.week_days, new_week_day, msg="Invalid Model Weekday after overwrite")
        self.assertEqual(model_section.user, self.db_user, msg="Model User is incorrect after overwrite with User")

    def testOverwriteRemoveUser(self):
        # Initial save
        self.db_user.save()
        self.db_section.user = self.db_user
        self.db_section.save()

        User.objects.get(email=self.db_user.email)
        Section.objects.get(id=self.db_section.id)

        # Definitions for changes
        new_type = SectionType.DISCUSSION
        new_location = "Potato Land"
        new_start_time = "10:00"
        new_end_time = "10:30"
        new_week_day = "M"

        # Set new values
        self.section.set_section_type(new_type)
        self.section.set_location(new_location)
        self.section.set_start_time(new_start_time)
        self.section.set_end_time(new_end_time)
        self.section.set_week_days(new_week_day)

        # Save again
        self.section.overwrite(self.db_section)

        # Get sect from DB
        model_section = Section.objects.get(id=self.db_section.id)

        self.assertEqual(model_section.section_type, new_type.db_alias,
                         msg="Invalid Model SectionType after overwrite()")
        self.assertEqual(model_section.location, new_location, msg="Invalid Model Location after overwrite()")
        self.assertEqual(model_section.start_time, new_start_time, msg="Invalid Model Start Time after overwrite()")
        self.assertEqual(model_section.end_time, new_end_time, msg="Invalid Model End Time after overwrite()")
        self.assertEqual(model_section.week_days, new_week_day, msg="Invalid Model Weekday after overwrite()")
        self.assertIsNone(model_section.user, msg="Model User is not None after overwrite removing User")

    def testOverwriteAddUser(self):
        # Initial save
        self.db_section.save()
        self.db_user.save()

        Section.objects.get(id=self.db_section.id)

        # Definitions for changes
        new_type = SectionType.DISCUSSION
        new_location = "Potato Land"
        new_start_time = "10:00"
        new_end_time = "10:30"
        new_week_day = "M"

        # Set new values
        self.section.set_section_type(new_type)
        self.section.set_location(new_location)
        self.section.set_start_time(new_start_time)
        self.section.set_end_time(new_end_time)
        self.section.set_week_days(new_week_day)
        self.section.assign_user(self.user)

        # Save again
        self.section.overwrite(self.db_section)

        # Get sect from DB
        model_section = Section.objects.get(id=self.db_section.id)

        self.assertEqual(model_section.section_type, new_type.db_alias, msg="Invalid Model SectionType after overwrite")
        self.assertEqual(model_section.location, new_location, msg="Invalid Model Location after overwrite")
        self.assertEqual(model_section.start_time, new_start_time, msg="Invalid Model Start Time after overwrite")
        self.assertEqual(model_section.end_time, new_end_time, msg="Invalid Model End Time after overwrite")
        self.assertEqual(model_section.week_days, new_week_day, msg="Invalid Model Weekday after overwrite")
        self.assertEqual(model_section.user, self.db_user, msg="Model User is incorrect after overwrite adding User")


# noinspection DuplicatedCode
class TestSectionFromModel(TestCase):
    u_email = "someone@example.com"
    u_account_type = AccountType.TA
    u_first_name = "Dink"
    u_last_name = "Smallwood"
    u_password = "password"
    u_phone = "999-999-9999"
    u_address = "123 Spooky Street"

    s_type = SectionType.LAB
    s_number = 401
    s_location = "Test"
    s_start_time = "8:00"
    s_end_time = "8:30"
    s_day = "M"

    def setUp(self):
        self.db_user = User()
        self.db_user.email = self.u_email
        self.db_user.account_type = self.u_account_type.name
        self.db_user.first_name = self.u_first_name
        self.db_user.last_name = self.u_last_name
        self.db_user.password = self.u_password
        self.db_user.phone_number = self.u_phone
        self.db_user.address = self.u_address

        self.db_section = Section()
        self.db_section.section_type = self.s_type.db_alias
        self.db_section.number = self.s_number
        self.db_section.location = self.s_location
        self.db_section.start_time = self.s_start_time
        self.db_section.end_time = self.s_end_time
        self.db_section.week_days = self.s_day

        self.db_user.save()
        self.db_section.save()

    # noinspection PyTypeChecker
    def testFromModelNone(self):
        with self.assertRaises(TypeError, msg="from_model did not raise error for None input"):
            SectionClass.from_model(None)

    # noinspection PyTypeChecker
    def testFromModelInvalidType(self):
        with self.assertRaises(TypeError, msg="from_model did not raise error for wrong-type input"):
            SectionClass.from_model(3)

    def testFromModelNoUser(self):
        section: SectionClass = SectionClass.from_model(self.db_section)

        self.assertEqual(self.s_type, section.get_section_type(), msg="Invalid SectionType after from_model")
        self.assertEqual(self.s_number, section.get_number(), msg="Invalid Number after from_model")
        self.assertEqual(self.s_location, section.get_location(), msg="Invalid Location after from_model")
        self.assertEqual(self.s_start_time, section.get_start_time(), msg="Invalid Start Time after from_model")
        self.assertEqual(self.s_end_time, section.get_end_time(), msg="Invalid End Time after from_model")
        self.assertEqual(self.s_day, section.get_week_days(), msg="Invalid WeekDay after from_model")
        self.assertIsNone(section.get_user(), msg="User was not None after from_model")

    def testFromModelYesUser(self):
        self.db_section.user = self.db_user
        self.db_section.save()

        section: SectionClass = SectionClass.from_model(self.db_section)

        self.assertEqual(self.s_type, section.get_section_type(), msg="Invalid SectionType after from_model")
        self.assertEqual(self.s_number, section.get_number(), msg="Invalid Number after from_model")
        self.assertEqual(self.s_location, section.get_location(), msg="Invalid Location after from_model")
        self.assertEqual(self.s_start_time, section.get_start_time(), msg="Invalid Start Time after from_model")
        self.assertEqual(self.s_end_time, section.get_end_time(), msg="Invalid End Time after from_model")
        self.assertEqual(self.s_day, section.get_week_days(), msg="Invalid WeekDay after from_model")

        # User assertions
        user: NewUserClass = section.get_user()
        self.assertIsNotNone(user, msg="User was None after from_model")
        self.assertEqual(user.email, self.u_email, msg="Invalid User Email after from_model")
        self.assertEqual(user.account_type, self.u_account_type, msg="Invalid User Email after from_model")
        self.assertEqual(user.first_name, self.u_first_name, msg="Invalid User First Name after from_model")
        self.assertEqual(user.last_name, self.u_last_name, msg="Invalid User Last Name after from_model")


class TestSectionDelete(TestCase):
    test_u_email = "someone@example.com"
    test_u_account_type = AccountType.TA
    test_u_first_name = "Dink"
    test_u_last_name = "Smallwood"
    test_u_password = "password"
    test_u_phone = "999-999-9999"
    test_u_address = "123 Spooky Street"

    test_s_type = SectionType.LAB
    test_s_number = 401
    test_s_location = "Test"
    test_s_start_time = "8:00"
    test_s_end_time = "8:30"
    test_s_day = "M"

    def setUp(self):
        self.db_section = Section()
        self.db_section.number = self.test_s_number
        self.db_section.section_type = self.test_s_type.db_alias
        self.db_section.location = self.test_s_location
        self.db_section.start_time = self.test_s_start_time
        self.db_section.end_time = self.test_s_end_time
        self.db_section.week_days = self.test_s_day
        self.db_section.save()

        self.user = NewUserClass(self.test_u_email, self.test_u_account_type, self.test_u_first_name,
                              self.test_u_last_name)

        self.section = SectionClass(self.test_s_type, self.test_s_number, self.test_s_location, self.test_s_start_time,
                                    self.test_s_end_time, self.test_s_day)

    def testDeleteSection(self):
        sectionID = self.db_section.id
        SectionClass.delete(sectionID)
        with self.assertRaises(ObjectDoesNotExist, msg="section should have been removed"):
            Section.objects.get(id=sectionID)

    def testDeleteSectionDoesNotExist(self):
        with self.assertRaises(RuntimeError, msg="section delete should raise error when section does not exist"):
            SectionClass.delete(5)

    def testDeleteSectionBadInput(self):
        with self.assertRaises(TypeError, msg="section delete should raise error on bad input"):
            SectionClass.delete("5")
        with self.assertRaises(TypeError, msg="section delete should raise error on no input"):
            SectionClass.delete(None)


