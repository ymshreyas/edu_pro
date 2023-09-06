from django.db import models
# Create your models here

class faculty_info(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=20)
    Designation = models.CharField(max_length=20,default='')
    name = models.CharField(max_length=20,default=' ')
    email = models.EmailField(max_length=20,unique=True,blank=True)
    user_type = models.CharField(max_length=20,default='1')
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    department = models.CharField(max_length=70,blank=True)
    specialisation = models.CharField(max_length=70,default='None')
    DOJ = models.DateField(blank=True,null=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    bachelor_degree = models.CharField(max_length=50,default=None)
    bachelor_instituition = models.CharField(max_length=50,default=None)
    bachelor_year = models.CharField(max_length=50,default=None)
    Masters_degree = models.CharField(max_length=50,default=None)
    Masters_instituition = models.CharField(max_length=50,default=None)
    Masters_year = models.CharField(max_length=50,default=None)
    Phd = models.CharField(max_length=50,default=None)
    Phd_instituition = models.CharField(max_length=50,default=None)
    Phd_year = models.CharField(max_length=50,default=None)

    def __str__(self):
        return self.name
    
class students(models.Model):
    username = models.CharField(max_length=10,primary_key=True)
    DOB = models.DateField()
    email = models.EmailField(max_length=250,unique=True)
    Name = models.CharField(max_length=250)
    Branch = models.CharField(max_length=250,null=True)
    semester = models.CharField(max_length=2,default='0')
    student_profile_pic = models.ImageField(upload_to='stud_profile_pics')
    counsellor = models.ForeignKey('faculty_info',on_delete=models.CASCADE)
    user_type = models.CharField(max_length=250,blank=True)

    def __str__(self):
        return self.username
    
class student_marks(models.Model):
    usn = models.CharField(max_length=20,default='')
    branch = models.CharField(max_length=100,default='')
    semester = models.PositiveIntegerField(default=1)
    sub_1_code = models.CharField(max_length=10,default='None')
    sub_1 = models.PositiveIntegerField()
    sub_2_code = models.CharField(max_length=10,default='None')
    sub_2 = models.PositiveIntegerField()
    sub_3_code = models.CharField(max_length=10,default='None')
    sub_3 = models.PositiveIntegerField()
    sub_4_code = models.CharField(max_length=10,default='None')
    sub_4 = models.PositiveIntegerField()
    sub_5_code = models.CharField(max_length=10,default='None')
    sub_5 = models.PositiveIntegerField()
    sub_6_code = models.CharField(max_length=10,default='None')
    sub_6 = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.usn} - {self.branch} - {self.semester}"

class stu_complaints(models.Model):
    name = models.CharField(max_length=100)
    usn = models.CharField(max_length=100,default="")
    faculty_name = models.CharField(max_length=100,default="")
    department = models.CharField(max_length=100,default="")
    complaint=models.TextField()

class fa_update_notification(models.Model):
    caption = models.CharField(max_length=100)
    type=models.CharField(max_length=20)
    information=models.CharField(max_length=500)
    date=models.DateField()
    semester=models.CharField(max_length=1,default="")

class Stu_Attendance(models.Model):
    student_name = models.ForeignKey(students, on_delete=models.CASCADE,default = '')
    date = models.DateField(auto_now_add=True)
    subject = models.CharField(max_length=50, default='None')
    is_present = models.BooleanField(default=False)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student_name} - {self.date} - {self.subject}"

    
class payments(models.Model):
    usn = models.ForeignKey('students',on_delete=models.CASCADE,default='')
    particulars=models.CharField(max_length=100)
    amount=models.CharField(max_length=100)
