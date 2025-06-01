from django.contrib import admin
from ProjectApp.models import User, Course, Section, SectionToCourse, TAToProfessor, TAToCourse
# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(SectionToCourse)
admin.site.register(TAToProfessor)
admin.site.register(TAToCourse)
