from django.db import models

# Create your models here.
class Patients(models.Model):
    FullName = models.CharField(max_length=150, null=True)
    MobileNumber = models.CharField(max_length=15, null=True)
    DateOfBirth = models.DateField(null=True)
    GovtIssuedId = models.CharField(max_length=150,null=True)
    GovtIssuedIdNo = models.CharField(max_length=150, null=True)
    FullAddress = models.CharField(max_length=350, null=True)
    State = models.CharField(max_length=200, null=True)
    RegistrationDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.FullName

class Phlebotomist(models.Model):
    EmpID = models.CharField(max_length=100, null=True)
    FullName = models.CharField(max_length=150, null=True)
    MobileNumber = models.CharField(max_length=15, null=True)
    RegDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.EmpID

class Testrecord(models.Model):
    OrderNumber = models.CharField(max_length=50, null=True)
    patient = models.ForeignKey(Patients,on_delete=models.CASCADE)
    TestType = models.CharField(max_length=250, null=True)
    TestTimeSlot = models.CharField(max_length=150, null=True)
    ReportStatus = models.CharField(max_length=200, null=True)
    FinalReport = models.FileField(null=True,blank=True)
    ReportUploadTime = models.CharField(max_length=150,null=True)
    RegistrationDate = models.DateTimeField(auto_now_add=True)
    phlebotomist = models.ForeignKey(Phlebotomist,on_delete=models.CASCADE, null=True)
    AssignedTime = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.OrderNumber

class Reporttracking(models.Model):
    testRecord = models.ForeignKey(Testrecord,on_delete=models.CASCADE)
    Remark = models.CharField(max_length=200, null=True)
    Status = models.CharField(max_length=150, null=True)
    PostingTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

class Contact(models.Model):
    name = models.CharField(max_length=100, null=True)
    emailid = models.CharField(max_length=50, null=True)
    contact = models.CharField(max_length=15, null=True)
    symptoms = models.CharField(max_length=150, null=True)
    message = models.CharField(max_length=300, null=True)
    msgdate = models.DateField(null=True)
    isread = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.emailid