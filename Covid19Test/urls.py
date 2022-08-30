"""Covid19Test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from covid.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('userindex', userindex, name='userindex'),
    path('newUserTesting', newUserTesting, name='newUserTesting'),
    path('registerUser', registerUser, name='registerUser'),
    path('register_UserDtls/<int:pid>', register_UserDtls, name='register_UserDtls'),
    path('patientReport', patientReport, name='patientReport'),
    path('viewPatient_reportDtls/<int:pid>', viewPatient_reportDtls, name='viewPatient_reportDtls'),
    path('logout',Logout,name='logout'),
    path('admin_login', admin_login, name='admin_login'),
    path('admin_home', admin_home, name='admin_home'),
    path('addPhlebotomist', addPhlebotomist, name='addPhlebotomist'),
    path('managePhlebotomist', managePhlebotomist, name='managePhlebotomist'),
    path('edit_Phlebotomist/<int:pid>', edit_Phlebotomist, name='edit_Phlebotomist'),
    path('delete_Phlebotomist/<int:pid>', delete_Phlebotomist, name='delete_Phlebotomist'),
    path('changePassword', changePassword, name='changePassword'),
    path('newTest', newTest, name='newTest'),
    path('viewTestingDtls/<int:pid>', viewTestingDtls,name='viewTestingDtls'),
    path('unread_queries', unread_queries, name='unread_queries'),
    path('read_queries', read_queries, name='read_queries'),
    path('view_queries/<int:pid>', view_queries, name='view_queries'),
    path('delete_contact/<int:pid>', delete_contact, name='delete_contact'),
    path('AssignedTest',AssignedTest, name='AssignedTest'),
    path('ontheway',ontheway, name='ontheway'),
    path('alltest',alltest, name='alltest'),
    path('samplecollected',samplecollected, name='samplecollected'),
    path('senttolab',senttolab, name='senttolab'),
    path('delivered',delivered, name='delivered'),
    path('delete_test/<int:pid>', delete_test, name='delete_test'),
    path('search',search, name='search'),
    path('betweendate_report',betweendate_report, name='betweendate_report'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
