"""TASchedulingProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ProjectApp.views import PersonalInfoViewer, Login, Home, PersonalInfoEditor, AccountInfoEditor, \
    AccountDeletion, AccountCreator, PCIViewer, AccountEditor, CourseInterface, \
    CourseCreator, SectionCreator, SectionEditorSupervisor, CoursesSchedule, \
    CourseEditor, PersonalSchedule, CourseDeletion, SectionInterface, SectionDelete, NotificationInterface

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view()),
    path('home.html/', Home.as_view()),
    path('home.html/home.html', Home.as_view()),
    path('home.html/personalinfoviewer.html', PersonalInfoViewer.as_view()),
    path('home.html/PCIviewer.html', PCIViewer.as_view()),
    path('home.html/personalinfoeditor.html', PersonalInfoEditor.as_view()),
    path('home.html/accountinfoeditor.html', AccountInfoEditor.as_view()),
    path('home.html/accountdeletion.html', AccountDeletion.as_view()),
    path('home.html/accountcreator.html', AccountCreator.as_view()),
    path('home.html/accounteditor.html', AccountEditor.as_view()),
    path('home.html/course.html/', CourseInterface.as_view()),
    path('home.html/coursecreator.html', CourseCreator.as_view()),
    path('home.html/coursesschedule.html', CoursesSchedule.as_view()),
    path('home.html/courseeditor.html', CourseEditor.as_view()),
    path('home.html/sectioncreator.html', SectionCreator.as_view()),
    path('home.html/supersectioneditor.html', SectionEditorSupervisor.as_view()),
    path('home.html/sectiondeletion.html', SectionDelete.as_view()),
    path('home.html/personalschedule.html', PersonalSchedule.as_view()),
    path('home.html/coursedeletion.html', CourseDeletion.as_view()),
    path('home.html/section.html', SectionInterface.as_view()),
    path('home.html/notification.html', NotificationInterface.as_view())
]
