from django.shortcuts import render, redirect
from django.views import View
from urllib.parse import urlencode

from UnitTests.test_UserClassTests import Visibility
from classes import new_user_class, course_class
from classes.course_class import CourseClass
from classes.new_user_class import NewUserClass, Category, PersonalInfoCategory, AccountType
from classes.section_class import SectionClass, SectionType
from classes.new_user_class import AccountType
from .models import User, Course, Section, SectionToCourse, ACCOUNT_TYPE, TAToCourse, SECTION_TYPE


class PersonalInfoViewer(View):
    def get(self, request):
        user2 = User.objects.get(email=request.session['user'])
        priv_data = NewUserClass.getPrivAccountData(self, user2, user2)
        hours_data = NewUserClass.getOfficeHoursData(self, user2)
        skills = NewUserClass.getSkills(self, user2)

        return render(request, "personalinfoviewer.html",
                      {"name": priv_data[0] + " " + priv_data[1],
                       "address": priv_data[4],
                       "phonenumber": priv_data[5],
                       "email": priv_data[2],
                       "position": priv_data[3],
                       "officehourslocation": hours_data[1],
                       "officehoursday": hours_data[0],
                       "officehourstime": hours_data[2],
                       "Skills": skills})

    def post(self, request):
        pass


class PersonalInfoEditor(View):
    def get(self, request):
        user = User.objects.get(email=request.session['user'])
        priv_data = NewUserClass.getPrivAccountData(self, user, user)
        hours_data = NewUserClass.getOfficeHoursData(self, user)
        skills = NewUserClass.getSkills(self, user)

        return render(request, "personalinfoeditor.html",
                      {"name": priv_data[0] + " " + priv_data[1],
                       "Address": priv_data[4],
                       "PhoneNumber": priv_data[5],
                       "email": priv_data[2],
                       "position": priv_data[3],
                       "room": hours_data[1],
                       "days": hours_data[0],
                       "times": hours_data[2],
                       "Skills": skills})

    def post(self, request):
        NewAddress = request.POST['NewAddress']
        NewPhoneNumber = request.POST['NewPhoneNumber']
        NewOfficeHoursRoom = request.POST['OfficeHoursRoom']
        NewOfficeHoursDays = request.POST['OfficeHoursDays']
        NewOfficeHoursTimes = request.POST['OfficeHoursTimes']
        newSkill = request.POST["Skills"]

        user = User.objects.get(email=request.session['user'])
        userObject = NewUserClass.from_model(user)

        try:
            userObject.set_office_hours_times(NewOfficeHoursTimes)
        except:
            if NewOfficeHoursTimes is None or NewOfficeHoursTimes == "":
                pass
            else:
                user = User.objects.get(email=request.session['user'])
                priv_data = NewUserClass.getPrivAccountData(self, user, user)
                hours_data = NewUserClass.getOfficeHoursData(self, user)
                skill = NewUserClass.getSkills(self, user)

                return render(request, "personalinfoeditor.html",
                              {"message": "An error was found -- please try again",
                               "Skills": skill,
                               "name": priv_data[0] + " " + priv_data[1],
                               "Address": priv_data[4],
                               "PhoneNumber": priv_data[5],
                               "email": priv_data[2],
                               "position": priv_data[3],
                               "room": hours_data[2],
                               "days": hours_data[0],
                               "times": hours_data[1]})
        try:
            userObject.set_office_hours_days(NewOfficeHoursDays)
        except:
            if NewOfficeHoursDays is None or NewOfficeHoursDays == "":
                pass
            else:
                user = User.objects.get(email=request.session['user'])
                priv_data = NewUserClass.getPrivAccountData(self, user, user)
                hours_data = NewUserClass.getOfficeHoursData(self, user)
                skill = NewUserClass.getSkills(self, user)

                return render(request, "personalinfoeditor.html",
                              {"message": "An error was found -- please try again",
                               "Skills": skill,
                               "name": priv_data[0] + " " + priv_data[1],
                               "Address": priv_data[4],
                               "PhoneNumber": priv_data[5],
                               "email": priv_data[2],
                               "position": priv_data[3],
                               "room": hours_data[2],
                               "days": hours_data[0],
                               "times": hours_data[1]})
        try:
            userObject.set_office_hours_room(NewOfficeHoursRoom)
        except:
            if NewOfficeHoursRoom is None or NewOfficeHoursRoom == "":
                pass
            else:
                user = User.objects.get(email=request.session['user'])
                priv_data = NewUserClass.getPrivAccountData(self, user, user)
                hours_data = NewUserClass.getOfficeHoursData(self, user)
                skill = NewUserClass.getSkills(self, user)

                return render(request, "personalinfoeditor.html",
                              {"message": "An error was found -- please try again",
                               "Skills": skill,
                               "name": priv_data[0] + " " + priv_data[1],
                               "Address": priv_data[4],
                               "PhoneNumber": priv_data[5],
                               "email": priv_data[2],
                               "position": priv_data[3],
                               "room": hours_data[2],
                               "days": hours_data[0],
                               "times": hours_data[1]})
        userObject.save()
        user = User.objects.get(email=request.session['user'])

        try:
            NewUserClass.addContactInfo(self, user, Category.phone, Visibility.private, NewPhoneNumber)
        except:
            if NewPhoneNumber is None or NewPhoneNumber == "":
                pass
            else:
                user = User.objects.get(email=request.session['user'])
                priv_data = NewUserClass.getPrivAccountData(self, user, user)
                hours_data = NewUserClass.getOfficeHoursData(self, user)
                skill = NewUserClass.getSkills(self, user)

                return render(request, "personalinfoeditor.html",
                              {"message": "An error was found -- please try again",
                               "Skills": skill,
                               "name": priv_data[0] + " " + priv_data[1],
                               "Address": priv_data[4],
                               "PhoneNumber": priv_data[5],
                               "email": priv_data[2],
                               "position": priv_data[3],
                               "room": hours_data[2],
                               "days": hours_data[0],
                               "times": hours_data[1]})
        try:
            NewUserClass.addContactInfo(self, user, Category.address, Visibility.private, NewAddress)
        except:
            if NewAddress is None or NewAddress == "":
                pass
            else:
                user = User.objects.get(email=request.session['user'])
                priv_data = NewUserClass.getPrivAccountData(self, user, user)
                hours_data = NewUserClass.getOfficeHoursData(self, user)
                skill = NewUserClass.getSkills(self, user)

                return render(request, "personalinfoeditor.html",
                              {"message": "An error was found -- please try again",
                               "Skills": skill,
                               "name": priv_data[0] + " " + priv_data[1],
                               "Address": priv_data[4],
                               "PhoneNumber": priv_data[5],
                               "email": priv_data[2],
                               "position": priv_data[3],
                               "room": hours_data[2],
                               "days": hours_data[0],
                               "times": hours_data[1]})
        try:
            NewUserClass.addSkill(self, user, newSkill)
        except:
            if newSkill is None or newSkill == "":
                pass
            else:
                user = User.objects.get(email=request.session['user'])
                priv_data = NewUserClass.getPrivAccountData(self, user, user)
                hours_data = NewUserClass.getOfficeHoursData(self, user)
                skill = NewUserClass.getSkills(self, user)

                return render(request, "personalinfoeditor.html",
                              {"message": "An error was found -- please try again",
                               "Skills": skill,
                               "name": priv_data[0] + " " + priv_data[1],
                               "Address": priv_data[4],
                               "PhoneNumber": priv_data[5],
                               "email": priv_data[2],
                               "position": priv_data[3],
                               "room": hours_data[2],
                               "days": hours_data[0],
                               "times": hours_data[1]})

        user.save()
        return render(request, "home.html", {"message": "Your information was updated successfully", "user": user})


class PCIViewer(View):
    def get(self, request):
        user = User.objects.get(email=request.session['user'])
        return render(request, "PCIviewer.html", {"users": User.objects.all(), "user": user})

    def post(self, request):
        store = None

        for user in User.objects.all():
            store = request.POST.get(user.email)
            if not store == None:
                break

        if store == 'Edit User Information':
            request.session['accountedit'] = user.email
            return redirect("accounteditor.html")

        if store == 'Delete User':
            request.session['accountdelete'] = user.email
            return redirect("accountdeletion.html")

        if 'Create' in request.POST:
            return render(request, "accountcreator.html", {"types": ACCOUNT_TYPE})


class AccountInterface(View):
    def get(self, request):

        account_type = User.objects.get(email=request.session['user']).account_type

        if not account_type == "Supervisor" and not account_type == "SU":
            return render(request, "home.html", {"message": "Marty says you do not have access to this page"})
        else:
            return render(request, "account.html", {})


class AccountCreator(View):
    def get(self, request):

        account_type = User.objects.get(email=request.session['user']).account_type

        if not account_type == "Supervisor" and not account_type == "SU":
            return render(request, "home.html", {"message": "Marty says you do not have access to this page"})

        return render(request, "accountcreator.html", {"types": ACCOUNT_TYPE})

    def post(self, request):
        firstName = request.POST["UserFirstName"]
        lastName = request.POST["UserLastName"]
        email = request.POST["UserEmail"]
        role = request.POST.get("UserRole", "")

        if firstName == "":
            return render(request, "accountcreator.html", {"message": "Invalid First Name", "types": ACCOUNT_TYPE})

        if lastName == "":
            return render(request, "accountcreator.html", {"message": "Invalid Last Name", "types": ACCOUNT_TYPE})

        if email == "":
            return render(request, "accountcreator.html", {"message": "Invalid Email", "types": ACCOUNT_TYPE})

        if role == "":
            return render(request, "accountcreator.html", {"message": "Invalid Role", "types": ACCOUNT_TYPE})

        account = User.objects.create(first_name=firstName, last_name=lastName, email=email, account_type=role,
                                      password="default")
        account.save()

        return render(request, "accountcreator.html",
                      {"message": "Account Successfully Created", "types": ACCOUNT_TYPE})


class AccountDeletion(View):
    def get(self, request):
        user = User.objects.get(email=request.session['accountdelete'])

        return render(request, "accountdeletion.html",
                      {"name": user.first_name + " " + user.last_name, "role": user.account_type, "email": user.email})

    def post(self, request):
        if 'Delete' in request.POST:

            user = User.objects.get(email=request.session['accountdelete'])
            supervisor = User.objects.get(email=request.session['user'])

            try:
                NewUserClass.deleteAccount(self, user, supervisor)
            except:
                return render(request, "accountdeletion.html",

                              {"name": user.first_name + " " + user.last_name,
                               "role": user.account_type,
                               "email": user.email,
                               "message": "User is assigned to course(s) or section(s)."})
            if (user == supervisor):
                return redirect('/')
        return redirect('/home.html/PCIviewer.html')


class AccountEditor(View):
    def get(self, request):
        user = User.objects.get(email=request.session['accountedit'])

        return render(request, "accounteditor.html",
                      {"FirstName": user.first_name, "LastName": user.last_name, "Email": user.email})

    def post(self, request):
        NewFirstName = request.POST['UserFirstName']
        NewLastName = request.POST['UserLastName']

        if NewFirstName == "":
            return render(request, "accounteditor.html", {"message": "Invalid First Name"})

        if NewLastName == "":
            return render(request, "accounteditor.html", {"message": "Invalid Last Name"})

        account = User.objects.get(email=request.session['accountedit'])

        try:
            NewUserClass.setUserInfo(self, account, PersonalInfoCategory.first_name, NewFirstName)
            NewUserClass.setUserInfo(self, account, PersonalInfoCategory.last_name, NewLastName)
        except:
            return redirect("accounteditor.html", {"message": "Input invalid: try again"})

        account.save()
        user = User.objects.get(email=request.session['user'])

        return render(request, "PCIviewer.html",
                      {"user": user,
                       "users": User.objects.all(),
                       "message": "Your change was successful!"})


class AccountInfoEditor(View):
    def get(self, request):
        return render(request, "accountinfoeditor.html", {})

    def post(self, request):
        CurrentPassword = request.POST['UserCurrentPassword']
        NewPassword = request.POST['UserNewPassword']
        ConfirmNewPassword = request.POST['UserConfirmNewPassword']
        user = User.objects.get(email=request.session['user'])

        if NewPassword == "" or ConfirmNewPassword == "":
            return render(request, "accountinfoeditor.html",
                          {"message": "Please enter new password."})

        if not NewPassword == ConfirmNewPassword or not CurrentPassword == user.password:
            return render(request, "accountinfoeditor.html",
                          {"message": "Incorrect password or passwords don't match."})

        try:
            NewUserClass.setPassword(self, user, NewPassword, CurrentPassword)
            return render(request, "accountinfoeditor.html", {"message": "Password Successfully Changed"})
        except:
            return request(render, "accountinfoeditor.html", {"message": "Incorrect Password"})


class Login(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        signInSuccess = NewUserClass.logIn(request.POST['Username'], request.POST['Password'])

        if signInSuccess:
            user = User.objects.get(email=request.POST['Username'])
            user_email = user.email
            request.session['user'] = user_email
            return redirect("/home.html")
        else:
            return render(request, "login.html", {"message": "Incorrect username or password"})


class Home(View):
    def get(self, request):
        user = User.objects.get(email=request.session['user'])
        return render(request, "home.html", {"user": user})


class CourseInterface(View):
    def get(self, request):
        user = User.objects.get(email=request.session['user'])
        return render(request, "course.html", {"user": user, "courses": Course.objects.all()})

    def post(self, request):
        store = None

        for course in Course.objects.all():
            store = request.POST.get(str(course.number))
            if not store == None:
                break

        if 'Create' in request.POST:
            return redirect("/home.html/coursecreator.html")

        if store == 'View Sections':
            request.session['courseToGetSectionsOf'] = course.number
            return redirect("/home.html/section.html")

        if store == 'Edit Course Information':
            request.session['courseedit'] = course.number
            return redirect("/home.html/courseeditor.html")

        if store == 'Delete Course':
            request.session['coursedelete'] = course.number
            return redirect("/home.html/coursedeletion.html")


class SectionInterface(View):
    def get(self, request):

        message_for_user = request.GET.get('message')

        if message_for_user is None:
            message_for_user = ""

        user = User.objects.get(email=request.session['user'])
        courseToFilter = Course.objects.get(number=request.session['courseToGetSectionsOf'])
        sectionList = CourseClass.getSections(self, courseToFilter)
        sections = []

        for i in sectionList:
            sections.append(i)

        return render(request, "section.html", {"message": message_for_user, "user": user, "sections": sections})

    def post(self, request):

        store = None

        for section in Section.objects.all():
            store = request.POST.get(str(section.number))
            if not store == None:
                break

        if store == 'Edit Section Information':
            request.session['sectionedit'] = section.id
            return redirect("supersectioneditor.html")

        if store == 'Delete Section':
            request.session['sectiondelete'] = section.id
            return redirect("sectiondeletion.html")

        if 'Create' in request.POST:
            request.session['addSectionToCourse'] =\
                Course.objects.get(number=request.session['courseToGetSectionsOf']).number

            return redirect("sectioncreator.html")


class CourseCreator(View):
    def get(self, request):

        account_type = User.objects.get(email=request.session['user']).account_type

        if not (account_type == "Supervisor"
                or account_type == "SU"
                or account_type == "Instructor"
                or account_type == "IN"):
            return render(request, "home.html", {"message": "Marty says you do not have access to this page"})

        return render(request, "coursecreator.html")

    def post(self, request):

        CourseName = request.POST.get("CourseName", "")
        CourseNumber = request.POST.get("CourseNumber", "")

        if CourseName == "":
            return render(request, "coursecreator.html", {"message": "Invalid Course Name"})

        if not CourseNumber.isdigit():
            return render(request, "coursecreator.html", {"message": "Invalid Course Number"})

        else:
            CourseNumber = int(CourseNumber)

        course = Course.objects.create(name=CourseName, number=CourseNumber)
        course.save()
        return render(request, "coursecreator.html", {"message": "Course Successfully Created"})


class SectionCreator(View):
    def get(self, request):

        account_type = User.objects.get(email=request.session['user']).account_type

        if not (account_type == "Supervisor" or account_type == "SU"):
            return render(request, "home.html", {"message": "You do not have access to this page"})
        else:
            return render(request, "sectioncreator.html", {"types": SECTION_TYPE})

    def post(self, request):

        number = request.POST.get('SectionNumber', "")

        if number == "":
            return render(request, "sectioncreator.html", {"message": "Invalid Section Number", "types": SECTION_TYPE})

        try:
            number = int(request.POST.get('SectionNumber'))
        except:
            return render(request, "sectioncreator.html", {"message": "Invalid Section Number", "types": SECTION_TYPE})

        sectionRoom = request.POST.get("Classroom", "")
        sectionStart = request.POST.get("StartTime", "")
        sectionEnd = request.POST.get("EndTime", "")
        sectionDays = request.POST.get("Days", "")
        sectionTypeStr = request.POST.get("sectionType", "")

        if sectionRoom == "":
            return render(request, "sectioncreator.html",
                          {"message": "Invalid Section Classroom", "types": SECTION_TYPE})

        if sectionTypeStr == "":
            return render(request, "sectioncreator.html", {"message": "Invalid Section Type", "types": SECTION_TYPE})

        if sectionStart == "":
            return render(request, "sectioncreator.html", {"message": "Invalid Start Time", "types": SECTION_TYPE})

        if sectionEnd == "":
            return render(request, "sectioncreator.html", {"message": "Invalid End Time", "types": SECTION_TYPE})

        if sectionDays == "":
            return render(request, "sectioncreator.html", {"message": "Invalid Days", "types": SECTION_TYPE})

        sectionTypeStr = request.POST.get("sectionType")
        sectionType = SectionType[sectionTypeStr.upper()]

        sectionExist = False
        sectionsOfCourse = None

        try:
            sectionsOfCourse = SectionToCourse.objects.filter(
                course=Course.objects.get(number=request.session['courseToGetSectionsOf']))
        except:
            pass

        if sectionsOfCourse is not None:
            for i in sectionsOfCourse:
                if i.section.number == int(request.POST['SectionNumber']):
                    sectionExist = True

        if sectionExist is False:
            try:
                sectionNum = int(request.POST['SectionNumber'])
            except:
                return render(request, "sectioncreator.html", {"message": "invalid number"})

            section = SectionClass(sectionType, sectionNum, request.POST['Classroom'],
                                   request.POST['StartTime'], request.POST['EndTime'], request.POST['Days'])
            section.save_new()
            sections = Section.objects.all()

            for i in sections:
                try:
                    sectionToCourseObj = SectionToCourse.objects.get(section=i)
                except:
                    sectionToCourseObj = None

                if sectionToCourseObj is None:
                    sectionToClass =SectionToCourse(
                        course=Course.objects.get(number=request.session['addSectionToCourse']),
                        section=i)
                    sectionToClass.save()
                    break

            return render(request, "sectioncreator.html", {"message": "new section created"})

        else:
            return render(request, "sectioncreator.html", {"message": "section already exists"})


class SectionEditorSupervisor(View):
    def get(self, request):
        sectionObj = Section.objects.get(id=request.session['sectionedit'])
        courseOfSection = Course.objects.get(number=request.session['courseToGetSectionsOf'])
        sectionNumber = sectionObj.number
        sectionLocation = sectionObj.location
        startTime = sectionObj.start_time
        endTime = sectionObj.end_time
        sectionType = sectionObj.section_type
        sectionDays = sectionObj.week_days

        TAToCourseObjs = TAToCourse.objects.filter(course=courseOfSection)
        listOfTAs = []

        for i in TAToCourseObjs:
            listOfTAs.append(i.ta)

        user = User.objects.get(email=request.session['user'])

        return render(request, "supersectioneditor.html",
                      {"user": user,
                       "sectionNumber": sectionNumber,
                       "sectionLocation": sectionLocation,
                       "startTime": startTime,
                       "endTime": endTime,
                       "sectionType": sectionType,
                       "sectionDays": sectionDays,
                       "tas": listOfTAs})

    def post(self, request):
        sectionObj = Section.objects.get(id=request.session['sectionedit'])

        try:
            newSectionNumber = request.POST['NewSectionNumber']
        except:
            newSectionNumber = sectionObj.number

        try:
            newLocation = request.POST['NewClassroom']
        except:
            newLocation = sectionObj.location

        try:
            newStartTime = request.POST['NewStartTime']
        except:
            newStartTime = sectionObj.start_time

        try:
            newEndTime = request.POST['NewEndTime']
        except:
            newEndTime = sectionObj.end_time

        try:
            newDays = request.POST['NewDays']
        except:
            newDays = sectionObj.week_days

        try:
            newUser = request.POST['NewTA']

            if newUser == "No TA" or newUser == "":
                newUser = None
            else:
                newUser = User.objects.get(email=request.POST['NewTA'])
        except:
            user = User.objects.get(email=request.session['user'])
            courseOfSection = Course.objects.get(number=request.session['courseToGetSectionsOf'])
            TAToCourseObjs = TAToCourse.objects.filter(course=courseOfSection)
            listOfTAs = []

            for i in TAToCourseObjs:
                listOfTAs.append(i.ta)

            return render(request, "supersectioneditor.html",
                          {"message": "Please select a TA or None",
                           "user": user,
                           "sectionNumber": sectionObj.number,
                           "sectionLocation": sectionObj.location,
                           "startTime": sectionObj.start_time,
                           "endTime": sectionObj.end_time,
                           "sectionType": sectionObj.section_type,
                           "sectionDays": sectionObj.week_days,
                           "tas": listOfTAs})

        try:
            section = SectionClass.from_model(sectionObj)
            section.set_number(int(newSectionNumber))
            section.set_location(newLocation)
            section.set_start_time(newStartTime)
            section.set_end_time(newEndTime)
            section.set_week_days(newDays)
        except RuntimeError or TypeError:
            user = User.objects.get(email=request.session['user'])
            courseOfSection = Course.objects.get(number=request.session['courseToGetSectionsOf'])
            TAToCourseObjs = TAToCourse.objects.filter(course=courseOfSection)
            listOfTAs = []

            for i in TAToCourseObjs:
                listOfTAs.append(i.ta)

            return render(request, "supersectioneditor.html",
                          {"message": "Invalid input",
                           "user": user,
                           "sectionNumber": sectionObj.number,
                           "sectionLocation": sectionObj.location,
                           "startTime": sectionObj.start_time,
                           "endTime": sectionObj.end_time,
                           "sectionType": sectionObj.section_type,
                           "sectionDays": sectionObj.week_days,
                           "tas": listOfTAs})

        if newUser is not None:
            if newUser.account_type == "TA" or newUser.account_type == 'AccountType.TA':
                accountType = AccountType.TA
            elif newUser.account_type == "Instructor":
                accountType = AccountType.INSTRUCTOR
            else:
                accountType = AccountType.SUPERVISOR

            temp_user = NewUserClass(email=newUser.email,
                                     account_type=accountType,
                                     first_name=newUser.first_name,
                                     last_name=newUser.last_name)

            section.assign_user(temp_user)

        elif section.get_user() is not None:
            section.remove_user()

        section.overwrite(sectionObj)

        sectionObj = Section.objects.get(id=request.session['sectionedit'])
        sectionNumber = sectionObj.number
        sectionLocation = sectionObj.location
        startTime = sectionObj.start_time
        endTime = sectionObj.end_time
        sectionType = sectionObj.section_type
        sectionDays = sectionObj.week_days

        user = User.objects.get(email=request.session['user'])
        courseOfSection = Course.objects.get(number=request.session['courseToGetSectionsOf'])
        TAToCourseObjs = TAToCourse.objects.filter(course=courseOfSection)
        listOfTAs = []

        for i in TAToCourseObjs:
            listOfTAs.append(i.ta)

        return render(request, "supersectioneditor.html",
                      {"message": "Section Successfully Updated",
                       "user": user,
                       "sectionNumber": sectionNumber,
                       "sectionLocation": sectionLocation,
                       "startTime": startTime,
                       "endTime": endTime,
                       "sectionType": sectionType,
                       "sectionDays": sectionDays,
                       "tas": listOfTAs})


class SectionDelete(View):
    def get(self, request):

        section_delete = Section.objects.get(id=request.session['sectiondelete'])
        course_of_section = Course.objects.get(number=request.session['courseToGetSectionsOf'])

        return render(request, 'sectiondeletion.html',
                      {'name': course_of_section.name,
                       'coursenum': course_of_section.number,
                       'sectionnum': section_delete.number,
                       'time': section_delete.start_time + "-" + section_delete.end_time,
                       'days': section_delete.week_days})

    def post(self, request):

        section_to_delete = Section.objects.get(id=request.session['sectiondelete'])
        section = SectionClass.from_model(section_to_delete)
        success = SectionClass.delete(section_to_delete.id)

        if success:
            query_string = urlencode({'message': "section deleted successfully"})
            url = '{}?{}'.format("section.html", query_string)
            return redirect(url)
        else:
            query_string = urlencode({'message': "could not delete section"})
            url = '{}?{}'.format("section.html", query_string)
            return redirect(url)


class CoursesSchedule(View):
    def get(self, request):
        courses = Course.objects.all()
        TAs = TAToCourse.objects.all()
        return render(request, "coursesschedule.html", {"courses": courses, "tasInCourse": TAs})


class CourseEditor(View):
    def get(self, request):

        courseedit = request.session['courseedit']
        course = Course.objects.get(number=courseedit)
        coursetas = list(NewUserClass.getTAs(self, course))
        addtas = list(User.objects.filter(account_type="TA"))

        for i in coursetas:
            if addtas.__contains__(i):
                addtas.remove(i)

        if not course.instructor is None:
            instructors = list(User.objects.filter(account_type="Instructor").exclude(email=course.instructor.email))
        else:
            instructors = list(User.objects.filter(account_type="Instructor"))

        return render(request, "courseeditor.html",
                      {"name": course.name,
                       "number": course.number,
                       "i": course.instructor,
                       "addtas": addtas,
                       "removetas": coursetas,
                       "instructors": instructors})

    def post(self, request):

        courseedit = request.session['courseedit']
        course = Course.objects.get(number=courseedit)
        coursetas = list(NewUserClass.getTAs(self, course))
        addtas = list(User.objects.filter(account_type="TA"))

        for i in coursetas:
            if addtas.__contains__(i):
                addtas.remove(i)

        if not course.instructor is None:
            instructors = list(User.objects.filter(account_type="Instructor").exclude(email=course.instructor.email))
        else:
            instructors = list(User.objects.filter(account_type="Instructor"))

        if 'Add' in request.POST:
            if request.POST.get('AddTA', "") == "":
                return render(request, "courseeditor.html",
                              {"message": "Please select a TA to add",
                               "name": course.name, "i": course.instructor,
                               "number": course.number,
                               "addtas": addtas, "removetas": coursetas,
                               "instructors": instructors})

            ta = User.objects.get(email=request.POST['AddTA'])
            tatocourse = TAToCourse.objects.create(course=course, ta=ta)
            tatocourse.save()
            coursetas.append(ta)

            if addtas.__contains__(ta):
                addtas.remove(ta)

            return render(request, "courseeditor.html",
                          {"message": "TA Successfully Added",
                           "name": course.name,
                           "number": course.number,
                           "i": course.instructor,
                           "addtas": addtas,
                           "removetas": coursetas,
                           "instructors": instructors})

        if 'Remove' in request.POST:
            if request.POST.get('RemoveTA', "") == "":
                return render(request, "courseeditor.html",
                              {"message": "Please select a TA to remove",
                               "name": course.name,
                               "number": course.number,
                               "i": course.instructor,
                               "addtas": addtas,
                               "removetas": coursetas,
                               "instructors": instructors})

            ta = User.objects.get(email=request.POST['RemoveTA'])
            tatocourse = TAToCourse.objects.filter(ta=ta).get(course=course)
            tatocourse.delete()
            addtas.append(ta)

            listOfSections = CourseClass.getSections(self, course)

            for i in listOfSections:
                if ta == i.user:
                    section = SectionClass.from_model(i)
                    section.remove_user()
                    section.overwrite(i)

            if coursetas.__contains__(ta):
                coursetas.remove(ta)

            return render(request, "courseeditor.html",
                          {"message": "TA Successfully Removed",
                           "name": course.name,
                           "number": course.number,
                           "i": course.instructor,
                           "addtas": addtas,
                           "removetas": coursetas,
                           "instructors": instructors})

        if 'ConfirmChanges' in request.POST:
            if request.POST['NewName'] == "":
                return render(request, "courseeditor.html",
                              {"message": "Invalid Course Name",
                               "name": course.name,
                               "number": course.number,
                               "i": course.instructor,
                               "addtas": addtas,
                               "removetas": coursetas,
                               "instructors": instructors})

            CourseClass.setName(self, course, request.POST['NewName'])

            if not request.POST['Instructor'] == "":
                CourseClass.assignInstructor(self, course, User.objects.get(email=request.POST['Instructor']))
            else:
                course.instructor = None

            course.save()

            return render(request, "courseeditor.html",
                          {"message": "Changes Successfully Saved!",
                           "name": course.name,
                           "number": course.number,
                           "i": course.instructor,
                           "addtas": addtas,
                           "removetas": coursetas,
                           "instructors": instructors})


class PersonalSchedule(View):
    def get(self, request):

        user = User.objects.get(email=request.session['user'])
        course_list = []

        if (user.account_type == 'Instructor'):
            course_list = NewUserClass.getCourse(self, user)

        section_list = NewUserClass.getSection(self, user)

        if (user.account_type == 'TA'):
            course_list = NewUserClass.getCourseTA(self, user)

        return render(request, 'personalschedule.html', {'courses': course_list, 'sections': section_list})

    def post(self, request):
        pass


class CourseDeletion(View):
    def get(self, request):
        coursedelete = request.session['coursedelete']
        course = Course.objects.get(number=coursedelete)
        return render(request, 'coursedeletion.html', {"name": course.name, "number": course.number})

    def post(self, request):
        if 'Confirm' in request.POST:
            coursedelete = request.session['coursedelete']
            course = Course.objects.get(number=coursedelete)
            course.delete()
            return redirect("course.html", {"message": "Course Successfully Deleted"})


class NotificationInterface(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
