from django.db import models

ACCOUNT_TYPE = (
    ("Supervisor", "Supervisor"),
    ("Instructor", "Instructor"),
    ("TA", "TA")
)

DAY = (
    ("M", "Monday"),
    ("T", "Tuesday"),
    ("W", "Wednesday"),
    ("R", "Thursday"),
    ("F", "Friday"),
    ("S", "Saturday"),
    ("U", "Sunday"),
    ("MWF", "Monday, Wednesday, Friday"),
    ("MW", "Monday, Wednesday"),
    ("TR", "Tuesday, Thursday")
)

SECTION_TYPE = (
    ("LECTURE", "Lecture"),
    ("LAB", "Lab"),
    ("DISCUSSION", "Discussion")
)


class User(models.Model):
    email = models.EmailField(primary_key=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(blank=True, max_length=10)
    address = models.CharField(blank=True, max_length=100)
    office_hours_days = models.CharField(blank=True, max_length=100)
    office_hours_times = models.CharField(blank=True, max_length=100)
    office_hours_room = models.CharField(blank=True, max_length=100)
    skills = models.CharField(blank=True, max_length=300)


class Course(models.Model):
    name = models.CharField(max_length=70, null=True)
    number = models.IntegerField(primary_key=True)
    instructor = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name='+')


class Section(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    section_type = models.CharField(max_length=30, choices=SECTION_TYPE, default="LAB")
    location = models.CharField(max_length=20)
    start_time = models.CharField(max_length=20)
    end_time = models.CharField(max_length=20)
    week_days = models.CharField(max_length=70, choices=DAY)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

class SectionToCourse(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, blank=False, on_delete=models.CASCADE, related_name='+')
    section = models.ForeignKey(Section, blank=False, on_delete=models.CASCADE, related_name='+')

class TAToCourse(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, blank=False, on_delete=models.CASCADE, related_name='+')
    ta = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='+')
