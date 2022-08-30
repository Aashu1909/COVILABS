import random
from .covid19api import getCovid
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import login,logout,authenticate
from datetime import date
from datetime import datetime
from django.db.models import Q
from django.db.models import Count

# Create your views here.

def index(request):
    error = ""
    # For the contact form 
    covid_data=getCovid()
    date1=covid_data[1]
    total_cases=covid_data[0]['total']
    new_cases=covid_data[0]['new']
    if request.method == 'POST':
        n = request.POST['name']
        e = request.POST['emailid']
        c = request.POST['contact']
        s = request.POST['symptoms']
        m = request.POST['message']
        try:
            Contact.objects.create(name=n, emailid=e, contact=c, symptoms=s, message=m, msgdate=date.today(),
                                   isread="no")
            error = "no"
        except:
            error = "yes"
    return render(request,'index.html', locals())

def unread_queries(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    contact = Contact.objects.filter(isread="no")
    return render(request,'unread_queries.html', locals())

def read_queries(request):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.filter(isread="yes")
    return render(request,'read_queries.html', locals())

def view_queries(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.get(id=pid)
    contact.isread = "yes"
    contact.save()
    return render(request,'view_queries.html', locals())

def delete_contact(request,pid):
    contact = Contact.objects.get(id=pid)
    contact.delete()
    return redirect('read_queries')

def userindex(request):

    patient = (Patients.objects.values('State').annotate(statecount=Count('State')).order_by())
    return render(request,'userindex.html',locals())

def newUserTesting(request):
    error = ""
    if request.method == "POST":
        fn = request.POST['FullName']
        mob = request.POST['MobileNumber']
        dob = request.POST['DateOfBirth']
        gid = request.POST['GovtIssuedId']
        gno = request.POST['GovtIssuedIdNo']
        fadd = request.POST['FullAddress']
        state = request.POST['State']
        orderno = str(random.randint(10000000, 99999999))
        testtype = request.POST['TestType']
        testtime = request.POST['TestTimeSlot']
        ReportStatus = "Not Processed yet"

        try:
            patient = Patients.objects.create(FullName=fn, MobileNumber=mob, DateOfBirth=dob, GovtIssuedId=gid, GovtIssuedIdNo=gno, FullAddress=fadd, State=state)
            Testrecord.objects.create(patient=patient,OrderNumber=orderno, TestType=testtype, TestTimeSlot=testtime, ReportStatus=ReportStatus)
            error = "no"
        except:
            error = "yes"
    return render(request,'newUserTesting.html', locals())

def registerUser(request):
    error=""
    if request.method == 'POST':
        sd = request.POST['searchdata']
    try:
        booking = Patients.objects.filter(Q(FullName=sd) | Q(MobileNumber=sd))
    except:
        booking = ""
    return render(request,'registerUser.html', locals())

def patientReport(request):
    error = ""
    if request.method == 'POST':
        sd = request.POST['searchdata']
        try:
            patients = Patients.objects.get(Q(MobileNumber=sd))
            test = Testrecord.objects.filter(patient=patients)
            return render(request, 'viewPatientReport.html', locals())
        except:
            test = ""
            return render(request, 'viewPatientReport.html', locals())
    return render(request,'patientReport.html', locals())

def viewPatient_reportDtls(request,pid):
    test = Testrecord.objects.get(id=pid)
    report1 = Reporttracking.objects.filter(testRecord=test)

    return render(request,'viewPatient_reportDtls.html', locals())

def register_UserDtls(request,pid):
    booking = Patients.objects.get(id=pid)

    if request.method == "POST":
        orderno = str(random.randint(10000000, 99999999))
        testtype = request.POST['TestType']
        testtime = request.POST['TestTimeSlot']
        ReportStatus = "Not Processed yet"

        try:
            Testrecord.objects.create(patient=booking,OrderNumber=orderno, TestType=testtype, TestTimeSlot=testtime, ReportStatus=ReportStatus)
            error = "no"
        except:
            error = "yes"

    return render(request, 'register_UserDtls.html', locals())

def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'admin_login.html', locals())

def admin_home(request):
    totaltest = Testrecord.objects.all().count()
    totalassigned = Testrecord.objects.filter(ReportStatus='Assigned').count()
    totalway = Testrecord.objects.filter(ReportStatus='On the Way for Collection').count()
    totalcollected = Testrecord.objects.filter(ReportStatus='Sample Collected').count()
    totallab = Testrecord.objects.filter(ReportStatus='Sent to Lab').count()
    totaldelivered = Testrecord.objects.filter(ReportStatus='Delivered').count()
    totalpatient = Patients.objects.all().count()
    totalphlebotomist = Phlebotomist.objects.all().count()
    return render(request, 'admin_home.html',locals())

def addPhlebotomist(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == "POST":
        empId = request.POST['EmpID']
        fname = request.POST['FullName']
        mob = request.POST['MobileNumber']
        try:
            Phlebotomist.objects.create(EmpID=empId, FullName=fname, MobileNumber=mob)
            error = "no"
        except:
            error = "yes"
    return render(request, 'addPhlebotomist.html', locals())

def managePhlebotomist(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    phlebotomist = Phlebotomist.objects.all()
    return render(request, 'managePhlebotomist.html', locals())

def edit_Phlebotomist(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    phlebotomist = Phlebotomist.objects.get(id=pid)
    if request.method=="POST":
        empID = request.POST['EmpID']
        fname = request.POST['FullName']
        mob = request.POST['MobileNumber']

        phlebotomist.EmpID = empID
        phlebotomist.FullName = fname
        phlebotomist.MobileNumber = mob

        try:
            phlebotomist.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_Phlebotomist.html', locals())

def delete_Phlebotomist(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    phlebotomist = Phlebotomist.objects.get(id=pid)
    phlebotomist.delete()
    return redirect('managePhlebotomist')

def newTest(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    test = Testrecord.objects.filter(ReportStatus='Not Processed yet')
    return render(request, 'newTest.html', locals())

def AssignedTest(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    test = Testrecord.objects.filter(ReportStatus='Assigned')
    return render(request, 'AssignedTest.html', locals())

def viewTestingDtls(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    test = Testrecord.objects.get(id=pid)
    report1 = Reporttracking.objects.filter(testRecord=test)
    testid = test.id
    phlebomist = Phlebotomist.objects.all()

    reportcount = Reporttracking.objects.filter(testRecord=test).count()
    try:
        if request.method == "POST":
            phlebotomistid = request.POST['assignto']
            ReportStatus = "Assigned"
            phlebotomist1 = Phlebotomist.objects.get(id=phlebotomistid)
            try:
                test.phlebotomist = phlebotomist1
                test.ReportStatus = ReportStatus
                now = datetime.now()
                test.AssignedTime = now.strftime("%m/%d/%Y %H:%M:%S")
                test.save()
                error = "no"
            except:
                error="yes"
    except:
        if request.method == "POST":
            ReportStatus = request.POST['ReportStatus']
            remark = request.POST['remark']

            try:
                reporttracking = Reporttracking.objects.create(testRecord=test,Remark=remark,Status=ReportStatus)
                test.ReportStatus = ReportStatus
                test.save()
                error1 = "no"
                try:
                    report = request.FILES['report']
                    test.FinalReport = report
                    now = datetime.now()
                    test.ReportUploadTime = now.strftime("%m/%d/%Y %H:%M:%S")
                    test.save()
                except:
                    pass
            except:
                error1 = "yes"
    return render(request,'viewTestingDtls.html', locals())

def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'changePassword.html', locals())

def Logout(request):
    logout(request)
    return redirect('index')


def ontheway(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    test = Testrecord.objects.filter(ReportStatus='On the Way for Collection')
    return render(request, 'ontheway.html', locals())

def alltest(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    test = Testrecord.objects.all()
    return render(request, 'alltest.html', locals())

def samplecollected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    test = Testrecord.objects.filter(ReportStatus='Sample Collected')
    return render(request, 'samplecollected.html', locals())

def senttolab(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    test = Testrecord.objects.filter(ReportStatus='Sent to Lab')
    return render(request, 'senttolab.html', locals())

def delivered(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    test = Testrecord.objects.filter(ReportStatus='Delivered')
    return render(request, 'delivered.html', locals())

def delete_test(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    patient = Patients.objects.get(id=pid)
    patient.delete()
    return redirect('alltest')


def search(request):
    sd = None
    patient = None
    if request.method == 'POST':
        sd = request.POST['searchdata']
    try:
        patient = Patients.objects.get(MobileNumber=sd)
        test = Testrecord.objects.filter(patient=patient)
    except:
        test = Testrecord.objects.filter(OrderNumber=sd)
    return render(request, 'search.html', locals())

def betweendate_report(request):
    if request.method == "POST":
        fd = request.POST['FromDate']
        td = request.POST['ToDate']
        test = Testrecord.objects.filter(Q(RegistrationDate__gte=fd) & Q(RegistrationDate__lte=td))
        return render(request, 'reportbtwdates.html', locals())
    return render(request, 'betweendate_report.html')