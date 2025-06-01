from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from classes.new_user_class import AccountType, Category, PersonalInfoCategory
from classes.new_user_class import NewUserClass
from ProjectApp.models import User, Course, TAToCourse, Section
import enum
from unittest import mock


class Visibility(enum.Enum):
    public = 1
    private = 2


# UserClassTests class, written by Wyatt K.
# Tests for the NewUserClass class.

class TestUserConstructor(TestCase):
    u_email = "test@example.com"
    u_type = AccountType.INSTRUCTOR
    u_first = "Skim"
    u_last = "Beeble"
    u_pass = "password"
    u_phone = "9998887777"
    u_address = "3400 N Maryland Avenue, Milwaukee WI, 53211"
    u_office_days = "MWF"
    u_office_times = "2:00-4:00 PM"
    u_office_room = "EMS 180"

    def testValid(self):
        user: NewUserClass = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)

        self.assertEqual(self.u_email, user.get_email(), "Wrong email after constructor.")
        self.assertEqual(self.u_type, user.get_account_type(), "Wrong AccountType after constructor.")
        self.assertEqual(self.u_first, user.get_first_name(), "Wrong first name after constructor.")
        self.assertEqual(self.u_last, user.get_last_name(), "Wrong last name after constructor.")

        self.assertEqual(None, user.get_address(), "Defined address after constructor.")
        self.assertEqual(None, user.get_office_hours_data()[0], "Defined office days after constructor.")
        self.assertEqual(None, user.get_office_hours_data()[1], "Defined office times after constructor.")
        self.assertEqual(None, user.get_office_hours_data()[2], "Defined office room after constructor.")

    # noinspection PyTypeChecker
    def testNoneTypes(self):
        none_input = None

        with self.assertRaises(TypeError, msg="Did not raise TypeError for None email"):
            NewUserClass(none_input, self.u_type, self.u_first, self.u_last)

        with self.assertRaises(TypeError, msg="Did not raise TypeError for None AccountType"):
            NewUserClass(self.u_email, none_input, self.u_first, self.u_last)

        with self.assertRaises(TypeError, msg="Did not raise TypeError for None first name"):
            NewUserClass(self.u_email, self.u_type, none_input, self.u_last)

        with self.assertRaises(TypeError, msg="Did not raise TypeError for None last name"):
            NewUserClass(self.u_email, self.u_type, self.u_first, none_input)

    # noinspection PyTypeChecker
    def testWrongTypes(self):
        int_input = 3

        with self.assertRaises(TypeError, msg="Did not raise TypeError for wrong-type email"):
            NewUserClass(int_input, self.u_type, self.u_first, self.u_last)

        with self.assertRaises(TypeError, msg="Did not raise TypeError for wrong-type AccountType"):
            NewUserClass(self.u_email, int_input, self.u_first, self.u_last)

        with self.assertRaises(TypeError, msg="Did not raise TypeError for wrong-type first name"):
            NewUserClass(self.u_email, self.u_type, int_input, self.u_last)

        with self.assertRaises(TypeError, msg="Did not raise TypeError for wrong-type last name"):
            NewUserClass(self.u_email, self.u_type, self.u_first, int_input)


class TestUserGetEmail(TestCase):
    u_email = "test@example.com"
    u_type = AccountType.INSTRUCTOR
    u_first = "Skim"
    u_last = "Beeble"
    u_pass = "password"
    u_phone = "9998887777"

    def setUp(self):
        self.user = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)

    def testGetEmail(self):
        self.assertEqual(self.u_email, self.user.get_email(), "Incorrect email from getter")


class TestUserGetAccountType(TestCase):
    u_email = "test@example.com"
    u_type = AccountType.INSTRUCTOR
    u_first = "Skim"
    u_last = "Beeble"
    u_pass = "password"
    u_phone = "9998887777"

    def setUp(self):
        self.user = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)

    def testGetAccountType(self):
        self.assertEqual(self.u_type, self.user.get_account_type(), "Incorrect AccountType from getter")


class TestUserSetAndGetFirstName(TestCase):
    u_email = "test@example.com"
    u_type = AccountType.INSTRUCTOR
    u_first = "Skim"
    u_last = "Beeble"
    u_pass = "password"
    u_phone = "9998887777"
    new_name = "Newname"

    def setUp(self):
        self.user = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)

    def testGetFirstName(self):
        self.assertEqual(self.u_first, self.user.get_first_name(), "Incorrect first name from getter")

    def testSetFirstNameValid(self):
        self.user.set_first_name(self.new_name)
        self.assertEqual(self.new_name, self.user.get_first_name(), "Incorrect first name from getter")

    # noinspection PyTypeChecker
    def testSetFirstNameNone(self):
        with self.assertRaises(TypeError, msg="set_first_name did not raise TypeError for None input"):
            self.user.set_first_name(None)

    def testSetFirstNameEmpty(self):
        with self.assertRaises(RuntimeError, msg="set_first_name did not raise TypeError for empty input"):
            self.user.set_first_name("")

    # noinspection PyTypeChecker
    def testSetFirstameWrongType(self):
        with self.assertRaises(TypeError, msg="set_first_name did not raise TypeError for wrong-type input"):
            self.user.set_first_name(3)


class TestUserSetAndGetLastName(TestCase):
    u_email = "test@example.com"
    u_type = AccountType.INSTRUCTOR
    u_first = "Skim"
    u_last = "Beeble"
    u_pass = "password"
    u_phone = "9998887777"
    new_name = "Newname"

    def setUp(self):
        self.user = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)

    def testGetLastName(self):
        self.assertEqual(self.u_last, self.user.get_last_name(), "Incorrect last name from getter")

    def testSetLastNameValid(self):
        self.user.set_last_name(self.new_name)
        self.assertEqual(self.new_name, self.user.get_last_name(), "Incorrect last name from getter")

    # noinspection PyTypeChecker
    def testSetLastNameNone(self):
        with self.assertRaises(TypeError, msg="set_last_name did not raise TypeError for None input"):
            self.user.set_last_name(None)

    def testSetLastNameEmpty(self):
        with self.assertRaises(RuntimeError, msg="set_last_name did not raise TypeError for empty input"):
            self.user.set_last_name("")

    # noinspection PyTypeChecker
    def testSetLastNameWrongType(self):
        with self.assertRaises(TypeError, msg="set_last_name did not raise TypeError for wrong-type input"):
            self.user.set_last_name(3)


class TestUserGetFullName(TestCase):
    u_email = "test@example.com"
    u_type = AccountType.INSTRUCTOR
    u_first = "Skim"
    u_last = "Beeble"
    u_pass = "password"
    u_phone = "9998887777"

    def setUp(self):
        self.user = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)

    def testGetFullName(self):
        full_name = self.u_first + " " + self.u_last
        self.assertEqual(full_name, self.user.get_full_name(), "Incorrect full name from getter")


class TestUserSetAndGetPassword(TestCase):
    u_email = "test@example.com"
    u_type = AccountType.INSTRUCTOR
    u_first = "Skim"
    u_last = "Beeble"
    u_pass = "default"
    u_phone = "9998887777"
    new_pass = "password2"

    def setUp(self):
        self.user = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)

    def testGetPassword(self):
        self.assertEqual(self.u_pass, self.user.get_password(), msg="Incorrect password from getter")

    def testSetPasswordValid(self):
        self.user.set_password(self.new_pass)
        self.assertEqual(self.new_pass, self.user.get_password(), msg="Incorrect password after setter")

    # noinspection PyTypeChecker
    def testSetPasswordNone(self):
        with self.assertRaises(TypeError, msg="TypeError not raised for None input on set_password"):
            self.user.set_password(None)

        self.assertEqual(self.u_pass, self.user.get_password(), msg="Password was changed after None set")

    # noinspection PyTypeChecker
    def testSetPasswordWrongType(self):
        with self.assertRaises(TypeError, msg="TypeError not raised for wrong-type input on set_password"):
            self.user.set_password(3)

        self.assertEqual(self.u_pass, self.user.get_password(), msg="Password was changed after wrong-type set")

    def testSetPasswordEmpty(self):
        with self.assertRaises(RuntimeError, msg="RuntimeError not raised for empty input on set_password"):
            self.user.set_password("")

        self.assertEqual(self.u_pass, self.user.get_password(), msg="Password was changed after blank set")


class TestUserSetAndGetPhoneNumber(TestCase):
    u_email = "test@example.com"
    u_type = AccountType.INSTRUCTOR
    u_first = "Skim"
    u_last = "Beeble"
    u_pass = "password"
    old_phone = "9998887777"
    new_phone = "5555555555"

    def setUp(self):
        self.user = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)
        self.user.phone_number = self.old_phone

    def testSetPhoneValid(self):
        self.user.set_phone_number(self.new_phone)
        self.assertEqual(self.new_phone, self.user.get_phone_number(), msg="Incorrect phone after setter")

    # noinspection PyTypeChecker
    def testSetPhoneNone(self):
        with self.assertRaises(TypeError, msg="set_phone_number did not raise TypeError for None input"):
            self.user.set_phone_number(None)

        self.assertEqual(self.old_phone, self.user.get_phone_number(), msg="Phone was changed to None after None set")

    # noinspection PyTypeChecker
    def testSetPhoneWrongType(self):
        with self.assertRaises(TypeError, msg="TypeError not raised for wrong-type input on set_phone_number"):
            self.user.set_phone_number(3)

        self.assertEqual(self.old_phone, self.user.get_phone_number(), msg="Phone was changed after wrong-type set")

    def testSetPhoneEmpty(self):
        with self.assertRaises(RuntimeError, msg="RuntimeError not raised for empty input on set_phone_number"):
            self.user.set_phone_number("")

        self.assertEqual(self.old_phone, self.user.get_phone_number(), msg="Phone was changed after blank set")


class TestUserSetAndGetAddress(TestCase):
    u_email = "test@example.com"
    u_type = AccountType.INSTRUCTOR
    u_first = "Skim"
    u_last = "Beeble"
    u_pass = "password"
    u_phone = "9998887777"
    old_address = "3400 N Maryland Avenue, Milwaukee WI, 53211"
    new_address = "3500 N Maryland Avenue, Milwaukee WI, 53211"

    def setUp(self):
        self.user = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)
        self.user2 = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)
        self.user2.set_address(self.old_address)
        print("Done with setup\n")

    def testGetAddressNone(self):
        self.assertEqual(None, self.user.get_address(), msg="Incorrect address from getter: expected None")

    def testSetAddressValidNoPrevious(self):
        self.user.set_address(self.new_address)
        self.assertEqual(self.new_address, self.user.get_address(), msg="Incorrect address after setter from None")

    def testSetAddressValidYesPrevious(self):
        self.user2.set_address(self.new_address)
        self.assertEqual(self.new_address, self.user2.get_address(),
                         msg="Incorrect address after setter from existing address")

    # noinspection PyTypeChecker
    def testSetAddressNone(self):
        print("None is str: " + str(isinstance(None, str)))

        with self.assertRaises(TypeError, msg="set_address None did not raise TypeError"):
            self.user2.set_address(None)

        self.assertEqual(self.old_address, self.user2.get_address(), msg="Address was changed to None after None set")

    # noinspection PyTypeChecker
    def testSetAddressWrongType(self):
        with self.assertRaises(TypeError, msg="TypeError not raised for wrong-type input on set_address"):
            self.user2.set_address(3)

        self.assertEqual(self.old_address, self.user2.get_address(), msg="Address was changed after wrong-type set")

    def testSetAddressEmpty(self):
        with self.assertRaises(RuntimeError, msg="RuntimeError not raised for empty input on set_address"):
            self.user2.set_address("")

        self.assertEqual(self.old_address, self.user2.get_address(), msg="Address was changed after blank set")

    def testRemoveAddress(self):
        self.user2.remove_address()
        self.assertEqual(None, self.user2.get_address(), msg="Address was not None after remove")


class TestUserGetOfficeHoursInfo(TestCase):
    u_email = "test@example.com"
    u_type = AccountType.INSTRUCTOR
    u_first = "Skim"
    u_last = "Beeble"
    u_pass = "password"
    u_phone = "9998887777"
    u_days = "MWF"
    u_room = "EMS E180"
    u_times = "2:00 PM - 4:00 PM"

    def setUp(self):
        self.user = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)
        self.user2 = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)

        self.user2.set_office_hours_days(self.u_days)
        self.user2.set_office_hours_room(self.u_room)
        self.user2.set_office_hours_times(self.u_times)

    def testGetNone(self):
        data = self.user.get_office_hours_data()
        self.assertEqual(None, data[0], msg="Office Hours days not None by default")
        self.assertEqual(None, data[1], msg="Office Hours room not None by default")
        self.assertEqual(None, data[2], msg="Office Hours times not None by default")

    def testGetSome(self):
        data = self.user2.get_office_hours_data()
        self.assertEqual(self.u_days, data[0], msg="Office Hours days incorrect")
        self.assertEqual(self.u_room, data[1], msg="Office Hours room incorrect")
        self.assertEqual(self.u_times, data[2], msg="Office Hours times incorrect")


class TestUserSetAndGetOfficeHoursDays(TestCase):
    u_email = "test@example.com"
    u_type = AccountType.INSTRUCTOR
    u_first = "Skim"
    u_last = "Beeble"
    u_pass = "password"
    u_phone = "9998887777"
    u_days = "MWF"
    u_days_2 = "TR"

    def setUp(self):
        self.user = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)
        self.user2 = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)

        self.user2.set_office_hours_days(self.u_days)

    def testSetDaysFromValid(self):
        self.user2.set_office_hours_days(self.u_days_2)
        self.assertEqual(self.u_days_2, self.user2.get_office_hours_data()[0],
                         msg="Days were not set properly from Valid to Valid")

    def testSetDaysFromNone(self):
        self.user.set_office_hours_days(self.u_days_2)
        self.assertEqual(self.u_days_2, self.user.get_office_hours_data()[0],
                         msg="Days were not set properly from None to Valid")

    # noinspection PyTypeChecker
    def testSetDaysNone(self):
        with self.assertRaises(TypeError, msg="set_office_hours_days did not raise TypeError for None input"):
            self.user2.set_office_hours_days(None)

        self.assertEqual(self.u_days, self.user2.get_office_hours_data()[0], msg="Days were changed on None input")

    def testRemove(self):
        self.user.remove_office_hours_days()
        self.assertEqual(None, self.user.get_office_hours_data()[0], msg="Days were not removed properly")


class TestUserSetAndGetOfficeHoursRoom(TestCase):
    u_email = "test@example.com"
    u_type = AccountType.INSTRUCTOR
    u_first = "Skim"
    u_last = "Beeble"
    u_pass = "password"
    u_phone = "9998887777"
    u_room = "EMS E180"
    u_room2 = "EMS E280"

    def setUp(self):
        self.user = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)
        self.user2 = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)

        self.user2.set_office_hours_room(self.u_room)

    def testSetRoomFromValid(self):
        self.user2.set_office_hours_room(self.u_room2)
        self.assertEqual(self.u_room2, self.user2.get_office_hours_data()[1],
                         msg="Room was not set properly from Valid to Valid")

    def testSetRoomFromNone(self):
        self.user.set_office_hours_room(self.u_room2)
        self.assertEqual(self.u_room2, self.user.get_office_hours_data()[1],
                         msg="Room was not set properly from None to Valid")

    # noinspection PyTypeChecker
    def testSetRoomNone(self):
        with self.assertRaises(TypeError, msg="set_office_hours_room did not raise TypeError for None input"):
            self.user2.set_office_hours_room(None)

        self.assertEqual(self.u_room, self.user2.get_office_hours_data()[1], msg="Room was changed on None input")

    def testRemove(self):
        self.user.remove_office_hours_room()
        self.assertEqual(None, self.user.get_office_hours_data()[1], msg="Room was not removed properly")


class TestUserSetOfficeHoursTimes(TestCase):
    u_email = "test@example.com"
    u_type = AccountType.INSTRUCTOR
    u_first = "Skim"
    u_last = "Beeble"
    u_pass = "password"
    u_phone = "9998887777"
    u_time = "2:00 PM - 4:00 PM"
    u_time2 = "3:00 PM - 5:00 PM"

    def setUp(self):
        self.user = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)
        self.user2 = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)

        self.user2.set_office_hours_times(self.u_time)

    def testSetTimesFromValid(self):
        self.user2.set_office_hours_times(self.u_time2)
        self.assertEqual(self.u_time2, self.user2.get_office_hours_data()[2],
                         msg="Times were not set properly from Valid to Valid")

    def testSetTimesFromNone(self):
        self.user.set_office_hours_times(self.u_time2)
        self.assertEqual(self.u_time2, self.user.get_office_hours_data()[2],
                         msg="Times were not set properly from None to Valid")

    # noinspection PyTypeChecker
    def testSetTimesNone(self):
        with self.assertRaises(TypeError, msg="set_office_hours_times did not raise TypeError for None input"):
            self.user2.set_office_hours_times(None)

        self.assertEqual(self.u_time, self.user2.get_office_hours_data()[2], msg="Times were changed on None input")

    def testRemove(self):
        self.user.remove_office_hours_times()
        self.assertEqual(None, self.user.get_office_hours_data()[2], msg="Times were not removed properly")


class TestUserSave(TestCase):
    u_email = "test@example.com"
    u_type = AccountType.INSTRUCTOR
    u_first = "Skim"
    u_last = "Beeble"
    u_pass = "password"
    u_phone = "9998887777"
    u_new_pass = "new"

    def setUp(self):
        self.user = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)

    def testSaveNew(self):
        self.assertRaises(ObjectDoesNotExist, msg="User was already saved")

        self.user.save()
        model_user = User.objects.get(email=self.u_email)

        UserTestUtils.compare_user_to_model(self.user, model_user)

    def testSaveOverwrite(self):
        self.assertRaises(ObjectDoesNotExist, msg="User was already saved")

        self.user.save()
        self.user.set_password(self.u_new_pass)
        self.user.save()

        model_user: User = User.objects.get(email=self.u_email)

        self.assertEqual(self.u_new_pass, model_user.password, msg="Password was not overwritten correctly.")


class TestUserFromModel(TestCase):
    u_email = "test@example.com"
    u_type = AccountType.INSTRUCTOR
    u_first = "Skim"
    u_last = "Beeble"
    u_pass = "password"
    u_phone = "9998887777"

    def setUp(self):
        self.user = NewUserClass(self.u_email, self.u_type, self.u_first, self.u_last)
        self.model_user = User(email=self.u_email, account_type=self.u_type.db_alias, first_name=self.u_first,
                               last_name=self.u_last)

    def testSuccess(self):
        converted_user: NewUserClass = NewUserClass.from_model(self.model_user)
        UserTestUtils.compare_user_to_model(converted_user, self.model_user)

    # noinspection PyTypeChecker
    def testNoneInput(self):
        with self.assertRaises(TypeError, msg="from_model with None input did not raise TypeError."):
            NewUserClass.from_model(None)

    # noinspection PyTypeChecker
    def testInvalidType(self):
        with self.assertRaises(TypeError, msg="from_model with wrong-type input did not raise TypeError."):
            NewUserClass.from_model(3)


class UserTestUtils:

    @staticmethod
    def compare_user_to_model(user: NewUserClass, model_user: User):
        if user.get_email() != NewUserClass.empty_string_to_none(model_user.email):
            raise RuntimeError("Incorrect email: " + str(user.get_email()) + " != " + str(model_user.email))

        if user.get_account_type().db_alias != NewUserClass.empty_string_to_none(model_user.account_type):
            raise RuntimeError("Incorrect account type: " + str(user.get_account_type().db_alias) + " != " + str(
                model_user.account_type))

        if user.get_first_name() != NewUserClass.empty_string_to_none(model_user.first_name):
            raise RuntimeError(
                "Incorrect first name: " + str(user.get_first_name()) + " != " + str(model_user.first_name))

        if user.get_last_name() != NewUserClass.empty_string_to_none(model_user.last_name):
            raise RuntimeError(
                "Incorrect last name: " + str(user.get_last_name()) + " != " + str(model_user.last_name))

        if NewUserClass.none_to_empty_string(user.get_address()) != model_user.address:
            raise RuntimeError(
                "Incorrect address: " + str(user.get_address()) + " != " + str(model_user.address))

        office = user.get_office_hours_data()

        if NewUserClass.none_to_empty_string(office[0]) != model_user.office_hours_days:
            raise RuntimeError(
                "Incorrect office days: " + str(office[0]) + " != " + str(model_user.office_hours_days))

        if NewUserClass.none_to_empty_string(office[1]) != model_user.office_hours_room:
            raise RuntimeError(
                "Incorrect office room: " + str(office[1]) + " != " + str(model_user.office_hours_room))

        if NewUserClass.none_to_empty_string(office[2]) != model_user.office_hours_times:
            raise RuntimeError(
                "Incorrect office times: " + str(office[2]) + " != " + str(model_user.office_hours_times))


class TestSetPassword(TestCase):
    def setUp(self):
        self.int_input = 2
        self.bool_input = True
        self.float_input = .5
        self.String_input_one = "one"
        self.String_input_two = "two"
        self.new_user = User(email="spoof@example.com", account_type=AccountType.TA, first_name="John", last_name="Doe",
                             password=self.String_input_one)
        self.new_user.save()

    def testSuccess(self):
        NewUserClass.setPassword(self, self.new_user, self.String_input_two, self.String_input_one)
        self.assertEqual(self.new_user.password, self.String_input_two)

    def testEqual(self):
        with self.assertRaises(RuntimeError, msg="New password = old password should raise RuntimeError"):
            NewUserClass.setPassword(self, self.new_user, self.String_input_one, self.String_input_one)
        self.assertEqual(self.new_user.password, self.String_input_one)

    def testBlank(self):
        with self.assertRaises(RuntimeError, msg="New password = blank space should raise RuntimeError"):
            NewUserClass.setPassword(self, self.new_user, "", self.String_input_one)
        self.assertEqual(self.new_user.password, self.String_input_one)

    def testInputInt(self):
        with self.assertRaises(TypeError, msg="Invalid input should should raise type error"):
            NewUserClass.setPassword(self, self.new_user, self.int_input, self.String_input_one)
        self.assertEqual(self.new_user.password, self.String_input_one)

    def testInputFloat(self):
        with self.assertRaises(TypeError, msg="Invalid input should should raise type error"):
            NewUserClass.setPassword(self, self.new_user, self.float_input, self.String_input_one)
        self.assertEqual(self.new_user.password, self.String_input_one)

    def testInputBool(self):
        with self.assertRaises(TypeError, msg="Invalid input should should raise type error"):
            NewUserClass.setPassword(self, self.new_user, self.bool_input, self.String_input_one)
        self.assertEqual(self.new_user.password, self.String_input_one)


class TestAddContactInfo(TestCase):
    def setUp(self):
        self.int_input = 2
        self.bool_input = True
        self.float_input = .5
        self.String_input_one = "one"
        self.String_input_two = "two"
        self.new_user = User(email="spoof@example.com", account_type=AccountType.TA, first_name="John", last_name="Doe",
                             phone_number="1234567890", address="3400 N Maryland Avenue, Milwaukee, WI, 53211")
        self.new_user.save()

    def testSuccess(self):
        NewUserClass.addContactInfo(self, self.new_user, Category.phone, Visibility.private, "0987654321")
        NewUserClass.addContactInfo(self, self.new_user, Category.address, Visibility.private,
                                    "3059 N Maryland Avenue, Milwaukee, WI, 53211")
        self.assertEqual(self.new_user.phone_number, "0987654321", "Phone number should change")
        self.assertEqual(self.new_user.address, "3059 N Maryland Avenue, Milwaukee, WI, 53211", "Address should change")

    def testInvalidInt(self):
        with self.assertRaises(TypeError, msg="Invalid int input type should raise type error"):
            NewUserClass.addContactInfo(self, self.new_user, Category.phone, Visibility.private, self.int_input)
            NewUserClass.addContactInfo(self, self.new_user, Category.address, Visibility.private, self.int_input)
        self.assertEqual(self.new_user.phone_number, "1234567890", "Phone number should not change")
        self.assertEqual(self.new_user.address, "3400 N Maryland Avenue, Milwaukee, WI, 53211",
                         "Address should not change")

    def testInvalidFloat(self):
        with self.assertRaises(TypeError, msg="Invalid float input type should raise type error"):
            NewUserClass.addContactInfo(self, self.new_user, Category.phone, Visibility.private, self.float_input)
            NewUserClass.addContactInfo(self, self.new_user, Category.address, Visibility.private, self.float_input)
        self.assertEqual(self.new_user.phone_number, "1234567890", "Phone number should not change")
        self.assertEqual(self.new_user.address, "3400 N Maryland Avenue, Milwaukee, WI, 53211",
                         "Address should not change")

    def testInvalidBool(self):
        with self.assertRaises(TypeError, msg="Invalid bool input type should raise type error"):
            NewUserClass.addContactInfo(self, self.new_user, Category.phone, Visibility.private, self.bool_input)
        with self.assertRaises(TypeError, msg="Invalid bool input type should raise type error"):
            NewUserClass.addContactInfo(self, self.new_user, Category.address, Visibility.private, self.bool_input)
        self.assertEqual(self.new_user.phone_number, "1234567890", "Phone number should not change")
        self.assertEqual(self.new_user.address, "3400 N Maryland Avenue, Milwaukee, WI, 53211",
                         "Address should not change")

    def testBadStringInput(self):
        with self.assertRaises(RuntimeError, msg="Bad input should raise runtime error"):
            NewUserClass.addContactInfo(self, self.new_user, Category.phone, Visibility.private,
                                        "123456789A")  # bad digit
        with self.assertRaises(RuntimeError, msg="Bad input should raise runtime error"):
            NewUserClass.addContactInfo(self, self.new_user, Category.phone, Visibility.private,
                                        "12345678901")  # too long
        with self.assertRaises(RuntimeError, msg="Bad input should raise runtime error"):
            NewUserClass.addContactInfo(self, self.new_user, Category.address, Visibility.private,
                                        "3400 N Maryland Avenue, Milwaukee WI")  # no zip
        with self.assertRaises(RuntimeError, msg="Bad input should raise runtime error"):
            NewUserClass.addContactInfo(self, self.new_user, Category.address, Visibility.private,
                                        "3400 N Maryland Avenue, Milwaukee 53211")  # no state
        self.assertEqual(self.new_user.phone_number, "1234567890", "Phone number should not change")
        self.assertEqual(self.new_user.address, "3400 N Maryland Avenue, Milwaukee, WI, 53211",
                         "Address should not change")

    def testCategoryEmail(self):
        with self.assertRaises(RuntimeError, msg="Category == email should raise runtime error"):
            NewUserClass.addContactInfo(self, self.new_user, Category.email, Visibility.public, "test")
        with self.assertRaises(RuntimeError, msg="Category == email should raise runtime error"):
            NewUserClass.addContactInfo(self, self.new_user, Category.email, Visibility.private, "test")


class TestGetContactInfo(TestCase):
    def setUp(self):
        self.String_input_one = "one"
        self.new_user = User(email="spoof@example.com", account_type=AccountType.TA, first_name="John", last_name="Doe",
                             phone_number="1234567890", address="3400 N Maryland Avenue, Milwaukee WI, 53211")
        self.new_user.save()
        self.int_input = 2
        self.bool_input = True
        self.float_input = .5
        self.String_input_one = "one"

    def testSuccess(self):
        self.assertEqual(NewUserClass.getContactInfo(self, self.new_user),
                         ["1234567890", "spoof@example.com", "3400 N Maryland Avenue, Milwaukee WI, 53211"],
                         "Should return list in format of [Phone, Email, Address]")

    def testBadInput(self):
        with self.assertRaises(TypeError, msg="Bad type should raise TypeError"):
            NewUserClass.getContactInfo(self, self.int_input)
        with self.assertRaises(TypeError, msg="Bad type should raise TypeError"):
            NewUserClass.getContactInfo(self, self.bool_input)
        with self.assertRaises(TypeError, msg="Bad type should raise TypeError"):
            NewUserClass.getContactInfo(self, self.float_input)
        with self.assertRaises(TypeError, msg="Bad type should raise TypeError"):
            NewUserClass.getContactInfo(self, self.String_input_one)


class TestLogIn(TestCase):
    def setUp(self):
        self.String_input_one = "one"
        self.String_input_two = "two"
        self.new_user = User(email="spoof@example.com", account_type=AccountType.TA, first_name="John", last_name="Doe",
                             password=self.String_input_one)
        self.int_input = 2
        self.bool_input = True
        self.float_input = .5
        self.new_user.save()

    def testSuccessfulLogIn(self):
        self.assertEqual(NewUserClass.logIn("spoof@example.com", self.String_input_one), True,
                         "Matching email and password should return True")

    def testBadPassword(self):
        self.assertEqual(NewUserClass.logIn("spoof@example.com", self.String_input_two), False,
                         "Bad password should return False")

    def testBadEmail(self):
        self.assertEqual(NewUserClass.logIn("spoofle@example.com", self.String_input_one), False,
                         "Email with no account should return False")

    def testBadFirstParameterInput(self):
        self.assertRaises(TypeError, NewUserClass.logIn, self.int_input, self.String_input_two,
                          "Bad input should raise type error")
        self.assertRaises(TypeError, NewUserClass.logIn, self.float_input, self.String_input_one,
                          "Bad input should raise type error")
        self.assertRaises(TypeError, NewUserClass.logIn, self.bool_input, self.String_input_one,
                          "Bad input should raise type error")

    def testBadSecondParameterInput(self):
        self.assertRaises(TypeError, NewUserClass.logIn, "spoof@example.com", self.int_input,
                          "Bad input should raise type error")
        self.assertRaises(TypeError, NewUserClass.logIn, "spoof@example.com", self.float_input,
                          "Bad input should raise type error")
        self.assertRaises(TypeError, NewUserClass.logIn, "spoof@example.com", self.bool_input,
                          "Bad input should raise type error")
        self.assertEqual(self.new_user.password, self.String_input_one, "Password should not change")


class TestSetUserInfo(TestCase):
    def setUp(self):
        self.String_input_one = "one"
        self.String_input_two = "two"
        self.new_user = User(email="spoof@example.com", account_type=AccountType.TA, first_name="John", last_name="Doe")
        self.int_input = 2
        self.bool_input = True
        self.float_input = .5
        self.new_user.save()

    def testSuccess(self):
        NewUserClass.setUserInfo(self, self.new_user, PersonalInfoCategory.first_name, "Jayson")
        NewUserClass.setUserInfo(self, self.new_user, PersonalInfoCategory.last_name, "Rock")
        self.assertEqual(self.new_user.first_name, "Jayson", "First name should have changed")
        self.assertEqual(self.new_user.last_name, "Rock", "Last name should have changed")

    def testNull(self):
        self.assertRaises(TypeError, NewUserClass.setUserInfo, self, None, "Jayson",
                          "Null parameter should raise type error")
        self.assertRaises(TypeError, NewUserClass.setUserInfo, self, PersonalInfoCategory.first_name, None,
                          "Null parameter should raise type error")
        self.assertRaises(TypeError, NewUserClass.setUserInfo, self, PersonalInfoCategory.last_name, None,
                          "Null parameter should raise type error")
        self.assertEqual(self.new_user.first_name, "John", "First name should not change")
        self.assertEqual(self.new_user.last_name, "Doe", "Last name should not change")

    def testEmpty(self):
        with self.assertRaises(RuntimeError, msg="Empty value should raise RuntimeError"):
            NewUserClass.setUserInfo(self, self.new_user, PersonalInfoCategory.first_name, "")
        with self.assertRaises(RuntimeError, msg="Empty value should raise RuntimeError"):
            NewUserClass.setUserInfo(self, self.new_user, PersonalInfoCategory.last_name, "")
        self.assertEqual(self.new_user.first_name, "John", "First name should not change")
        self.assertEqual(self.new_user.last_name, "Doe", "Last name should not change")

    def testInvalidInputCategory(self):
        with self.assertRaises(TypeError, msg="Invalid input type should raise type error"):
            NewUserClass.setUserInfo(self, self.new_user, self.int_input, "Jayson")
            NewUserClass.setUserInfo(self, self.new_user, self.float_input, "Jayson")
            NewUserClass.setUserInfo(self, self.new_user, self.bool_input, "Jayson")

    def testInvalidInputValue(self):
        with self.assertRaises(TypeError, msg="Invalid input type should raise type error"):
            NewUserClass.setUserInfo(self, PersonalInfoCategory.first_name, self.int_input)
            NewUserClass.setUserInfo(self, PersonalInfoCategory.last_name, self.int_input)
            NewUserClass.setUserInfo(self, PersonalInfoCategory.first_name, self.float_input)
            NewUserClass.setUserInfo(self, PersonalInfoCategory.last_name, self.float_input)
            NewUserClass.setUserInfo(self, PersonalInfoCategory.first_name, self.bool_input)
            NewUserClass.setUserInfo(self, PersonalInfoCategory.last_name, self.bool_input)
        self.assertEqual(self.new_user.first_name, "John", "First name should not change")
        self.assertEqual(self.new_user.last_name, "Doe", "Last name should not change")


class TestGetUserInfo(TestCase):
    def setUp(self):
        self.String_input_one = "one"
        self.String_input_two = "two"
        self.int_input = 2
        self.bool_input = True
        self.float_input = .5
        self.new_user = User(email="spoof@example.com", account_type=AccountType.TA, first_name="John", last_name="Doe")

    def testSuccess(self):
        self.assertEqual(NewUserClass.getUserInfo(self, self.new_user, PersonalInfoCategory.email), "spoof@example.com")
        self.assertEqual(NewUserClass.getUserInfo(self, self.new_user, PersonalInfoCategory.last_name), "Doe")
        self.assertEqual(NewUserClass.getUserInfo(self, self.new_user, PersonalInfoCategory.first_name), "John")

    def testNoneType(self):
        with self.assertRaises(TypeError, msg="None type should raise type error"):
            NewUserClass.getUserInfo(self, self.new_user, None)
        with self.assertRaises(TypeError, msg="None type should raise type error"):
            NewUserClass.getUserInfo(self, None, PersonalInfoCategory.first_name)

    def testBadInputType(self):
        self.assertRaises(TypeError, NewUserClass.getUserInfo, self, self.new_user, self.int_input,
                          msg="None type should raise type error")
        self.assertRaises(TypeError, NewUserClass.getUserInfo, self, self.new_user, self.float_input,
                          msg="None type should raise type error")
        self.assertRaises(TypeError, NewUserClass.getUserInfo, self, self.new_user, self.bool_input,
                          msg="None type should raise type error")


class TestDeleteAccount(TestCase):
    def setUp(self):
        self.String_input_one = "one"
        self.String_input_two = "two"
        self.new_user = User(email="spoof@example.com", account_type=AccountType.TA, first_name="John", last_name="Doe")
        self.supervisor = User(email="supervisor@uwm.edu", account_type=AccountType.SUPERVISOR, first_name="Jayson",
                               last_name="Rock")
        self.int_input = 2
        self.bool_input = True
        self.float_input = .5
        self.new_user.save()

    def testNoneInput(self):
        with self.assertRaises(TypeError, msg="Deleting someone that doesnt exist should raise error"):
            NewUserClass.deleteAccount(self, None, self.supervisor)

    def testBadInput(self):
        self.assertRaises(TypeError, NewUserClass.deleteAccount, self, self.int_input, self.supervisor,
                          "Invalid type should raise type error")
        self.assertRaises(TypeError, NewUserClass.deleteAccount, self, self.float_input, self.supervisor,
                          "Invalid type should raise type error")
        self.assertRaises(TypeError, NewUserClass.deleteAccount, self, self.bool_input, self.supervisor,
                          "Invalid type should raise type error")
        self.assertRaises(TypeError, NewUserClass.deleteAccount, self, self.new_user, self.int_input,
                          "Invalid type should raise type error")
        self.assertRaises(TypeError, NewUserClass.deleteAccount, self, self.new_user, self.float_input,
                          "Invalid type should raise type error")
        self.assertRaises(TypeError, NewUserClass.deleteAccount, self, self.new_user, self.bool_input,
                          "Invalid type should raise type error")


class TestGetPrivAccountData(TestCase):
    def setUp(self):
        self.password = "default_password"
        self.address = "3400 N Maryland Avenue, Milwaukee WI, 53211"

        self.user_supervisor = User(email="jndoe@example.com", account_type=AccountType.SUPERVISOR, first_name="Jane",
                                    last_name="Doe", address=self.address, phone_number="9998887777",
                                    password=self.password)
        self.user_instructor = User(email="jdoe@example.com", account_type=AccountType.INSTRUCTOR, first_name="John",
                                    last_name="Doe", address=self.address, phone_number="6665554444",
                                    password=self.password)
        self.user_TA = User(email="jkdoe@example.com", account_type=AccountType.TA, first_name="Jake", last_name="Doe",
                            address=self.address, phone_number="3332221111", password=self.password)

        self.userDataList = ["Jake", "Doe", "jkdoe@example.com", AccountType.TA, self.address, "3332221111"]

    def test_TAGetData(self):
        with self.assertRaises(RuntimeError, msg="TA does not have permission to get private account data"):
            NewUserClass.getPrivAccountData(self, self.user_instructor, self.user_TA)

    def test_TAGetOwnData(self):
        self.assertEqual(NewUserClass.getPrivAccountData(self, self.user_TA, self.user_TA), self.userDataList)

    def test_InvalidInputStringGetData(self):
        with self.assertRaises(TypeError, msg="invalid user type"):
            NewUserClass.getPrivAccountData(self, "Yes I am real user")

    def test_InvalidInputIntGetData(self):
        with self.assertRaises(TypeError, msg="invalid user type"):
            NewUserClass.getPrivAccountData(self, 1223)

    def test_InvalidInputEmptyGetData(self):
        with self.assertRaises(TypeError, msg="invalid user type"):
            NewUserClass.getPrivAccountData(self, None)


class TestGetCourse(TestCase):
    def setUp(self):
        self.new_user = User.objects.create(email="spoof@example.com", account_type=AccountType.TA, first_name="John",
                                            last_name="Doe")
        self.new_course = Course.objects.create(name="CourseName", number=123)
        self.ta_to_course = TAToCourse.objects.create(course=self.new_course, ta=self.new_user)

    def testSuccess(self):
        course = NewUserClass.getCourseTA(self, self.new_user)
        self.assertEqual(course[0], self.new_course, msg="Course gotten does not match given course")

    def testNotUser(self):
        with self.assertRaises(TypeError, msg="Wrongt ype should return typeerror"):
            NewUserClass.getCourseTA(self, self.new_course)

    def testNull(self):
        with self.assertRaises(TypeError, msg="None type should return typeerror"):
            NewUserClass.getCourseTA(self, None)


class TestGetSection(TestCase):
    def setUp(self):
        self.new_user = User.objects.create(email="spoof@example.com", account_type=AccountType.TA, first_name="John",
                                            last_name="Doe")
        self.new_section = Section.objects.create(section_type="Lecture", number="401", week_days="MW",
                                                  start_time="2:00:00pm",
                                                  end_time="4:00:00pm", location="EMS 270")

    def testSuccess(self):
        self.new_section.user = self.new_user
        self.new_section.save()

        section_list = NewUserClass.getSection(self, self.new_user)
        self.assertEqual(section_list[0], self.new_section, msg="Section gotten does not match given course")
        self.assertEqual(len(section_list), 1, msg="Section List size is incorrect")

    def testSuccessEmpty(self):
        section_list = NewUserClass.getSection(self, self.new_user)
        self.assertEqual(len(section_list), 0, msg="Section List size is incorrect")

    def testNotUser(self):
        with self.assertRaises(TypeError, msg="Wrong type should return type error"):
            NewUserClass.getCourse(self, self.new_section)

    def testNull(self):
        with self.assertRaises(TypeError, msg="Wrong type should return type error"):
            NewUserClass.getCourse(self, None)
