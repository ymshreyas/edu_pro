from django.shortcuts import render,redirect
from edu_app.forms import Facultyprofileinfoforms
from edu_app.models import students,student_marks,fa_update_notification,stu_complaints,faculty_info,Stu_Attendance,payments
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from datetime import date
import re
# Create your views here.

def check_username_exists(username):
    try:
        user = faculty_info.objects.get(username=username)
        return False
    except faculty_info.DoesNotExist:
        return True
def check_usn_exists(usn):
    try:
        user = student_marks.objects.get(usn=usn)
        return False
    except student_marks.DoesNotExist:
        return True
def check_password_exists(password):
    try:
        user = faculty_info.objects.get(password=password)
        return False
    except faculty_info.DoesNotExist:
        return True

def validate(password):
    # Define the regex pattern for the password
    pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d*#@!]{8,}$"

    # Match the password against the pattern
    match = re.match(pattern, password)

    if match:
        return True
    else:
        return False
    
def landing(request):
    return render(request,'edu_app/landing_page.html')


def register(request):
    registered = False
    if request.method == 'POST':
        profile_form = Facultyprofileinfoforms(data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if(validate(password) and check_username_exists(username) and check_password_exists(password)):
            if  profile_form.is_valid():
                profile = profile_form.save(commit=False)
                if 'profile_pic' in request.FILES:
                    profile.profile_pic = request.FILES['profile_pic']
                profile.save()
                registered = True 
            else:
                print(profile_form.errors)
        else:
            messages.success(request,"Looks like there's already an account that exists or your password must be weak, password must atleast contain 8 characters starting with capital letters followed by combination of small letters numbers and special characters")
            return redirect('register')
    else:
        profile_form = Facultyprofileinfoforms()
    
    return render(request,'edu_app/registration.html',{'profile_form':profile_form,'registered': registered})


def user_login(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            usn = request.POST['username']
            user_type = request.POST['usertype']
            user = authenticate(request,username=username,password=password)
            if user_type == '1':
                exists = faculty_info.objects.filter(username=username,password=password,user_type=user_type).exists()
                if user is not None and exists:
                    login(request,user)
                    fact = faculty_info.objects.filter(username=username)
                    return render(request,'edu_app/Faculty.html',{'fact':fact}) 
                else:
                    print("Someone tried to login and failed")
                    print(f"Username : {username} and password : {password}")
                    messages.success(request,"Invalid username or password, try again...")
                    return redirect('user_login')
            elif user_type == '2':
                DOB = request.POST['password']
                exist = students.objects.filter(username=username,DOB=DOB,user_type=user_type).exists()
                if user is not None and exist:
                    studs = students.objects.filter(username=username)
                    faculty = faculty_info.objects.all()
                    plot = student_marks.objects.filter(usn=usn)
                    context = {
                        "studs" : studs,
                        "plot" : plot,
                        "faculty" : faculty
                    }
                    login(request,user)
                    return render(request,'edu_app/student.html',context) 
                else:
                    print("Someone tried to login and failed")
                    print(f"Username : {username} and password : {password}")
                    messages.success(request,"Invalid username or password, try again...")
                    return redirect('user_login')
        else:
            return render(request,'edu_app/login.html',{})
    except ValidationError:
        messages.success(request,"Invalid username or password, try again...")
        return redirect('user_login')
    
def complaints(request):
    if request.method == "POST":
        name=request.POST["name"]
        usn=request.POST["usn"]
        complaint=request.POST["complaint"]
        faculty_name=request.POST["faculty_name"]
        department=request.POST["department"]
        obj=stu_complaints(name=name, usn=usn, complaint=complaint,faculty_name=faculty_name,department=department)
        obj.save()
        messages.success(request,'Complaint submitted successfully')
        return redirect('complaints')
    return render(request,'edu_app/student_complaint.html',{})

def payment_view(request):
    student_username = request.user.username
    
    data = payments.objects.filter(usn__username=student_username)
    return render(request, 'edu_app/payments.html', {'data': data})

def notification_update(request):
    if request.method == "POST":
        caption=request.POST["caption"]
        type=request.POST["type"]
        information=request.POST["information"]
        date=request.POST["date"]
        semester=request.POST["semester"]
        obj=fa_update_notification(caption=caption, type=type, information=information, date=date,semester=semester)
        obj.save()
        messages.success(request, 'Notification submitted successfully.')
        return redirect('update_notification')
    else:
        return render(request,'edu_app/update_notification.html',{})

def take_attendance(request):
    selected_subject = request.GET.get('subject', '')
    selected_semester = request.GET.get('semester', '')
    faculty_username = request.user.username

    faculty = faculty_info.objects.get(username=faculty_username)
    faculty_department = faculty.department

    student_list = students.objects.filter(Branch=faculty_department, semester=selected_semester)

    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        for student in student_list:
            is_present = request.POST.get(student.username) == "on" or request.POST.get(f"{student.username}_checked") == "on"
            attendance, created = Stu_Attendance.objects.get_or_create(student_name=student, date=date.today(), subject=selected_subject)
            attendance.is_present = is_present
            attendance.start_time = start_time
            attendance.end_time = end_time
            attendance.save()
        messages.success(request,'Attendance submitted successfully')
        return redirect('take_attendance')

    subjects = []
    if selected_semester=="1" or selected_semester=="2":
        subjects=["22MAT111", "22CPC112","22CHE113", "22BEC114", "22EGD115","22MAT121", "22PHY122", "22BEE123", "22BES124", "22CPC125"]
    elif faculty_department == "Computer Science and Engineering" and (selected_semester=="3" or selected_semester=="4"):
        subjects = ["21MAI131", "21CSE132", "21CSE133", "21CSE134", "21CSE135", "21CSE136", "21MAI141", "21CSE142", "21CSE143", "21CSE144", "21CSE145", "21CSE146"]
    elif faculty_department == "Computer Science and Engineering" and selected_semester=="5" or selected_semester=="6":
        subjects = ["20CSE151", "20CSE152", "20CSE153", "20CSE154", "20CSE155", "20CSE161", "20CSE162", "20CSE163", "20CSE164", "20CSE165"]
    elif faculty_department == "Computer Science and Engineering" and selected_semester=="7" or selected_semester=="8":
        subjects = ["19CSE171", "19CSE172", "19CSE173", "19CSE174", "19CSE175", "19CSE181", "19CSE182", "19CSE183"]
        
    elif faculty_department == "Infromation Science and Engineering" and selected_semester=="3" or selected_semester=="4":
        subjects = ["21MAI131", "21ISE132", "21ISE133", "21ISE134", "21ISE135", "21ISE136", "21MAI141", "21ISE142", "21ISE143", "21ISE144", "21ISE145", "21ISE146"]
    elif faculty_department == "Infromation Science and Engineering" and selected_semester=="5" or selected_semester=="6":
        subjects = ["20ISE151", "20ISE152", "20ISE153", "20ISE154", "20ISE155", "20ISE161", "20ISE162", "20ISE163", "20ISE164", "20ISE165"]
    elif faculty_department == "Infromation Science and Engineering" and selected_semester=="7" or selected_semester=="8":
        subjects = ["19ISE171", "19ISE172", "19ISE173", "19ISE174", "19ISE175", "19ISE181", "19ISE182", "19ISE183"]
        
    elif faculty_department == "Artifical Intelligence and machine learning" and selected_semester=="3" or selected_semester=="4":
        subjects = ["21MAI131", "21AIML132", "21AIML133", "21AIML134", "21AIML135", "21AIML136", "21MAI141", "21AIML142", "21AIML143", "21AIML144", "21AIML145", "21AIML146"]
    elif faculty_department == "Artifical Intelligence and machine learning" and selected_semester=="5" or selected_semester=="6":
        subjects = ["20AIML151", "20AIML152", "20AIML153", "20AIML154", "20AIML155", "20AIML161", "20AIML162", "20AIML163", "20AIML164", "20AIML165"]
    elif faculty_department == "Artifical Intelligence and machine learning" and selected_semester=="7" or selected_semester=="8":
        subjects = ["19AIML171", "19AIML172", "19AIML173", "19AIML174", "19AIML175", "19AIML181", "19AIML182", "19AIML183"]

    elif faculty_department == "Electronics and Communication Engineering" and selected_semester=="3" or selected_semester=="4":
        subjects = ["21MAI131", "21ECE132", "21ECE133", "21ECE134", "21ECE135", "21ECE136", "21MAI141", "21ECE142", "21ECE143", "21ECE144", "21ECE145", "21ECE146"]
    elif faculty_department == "Electronics and Communication Engineering" and selected_semester=="5" or selected_semester=="6":
        subjects = ["20ECE151", "20ECE152", "20ECE153", "20ECE154", "20ECE155", "20ECE161", "20ECE162", "20ECE163", "20ECE164", "20ECE165"]
    elif faculty_department == "Electronics and Communication Engineering" and selected_semester=="7" or selected_semester=="8":
        subjects = ["19ECE171", "19ECE172", "19ECE173", "19ECE174", "19ECE175", "19ECE181", "19ECE182", "19ECE183"]
    
    elif faculty_department == "Electrical and Electronics engineering" and selected_semester=="3" or selected_semester=="4":
        subjects = ["21MAI131", "21EEE132", "21EEE133", "21EEE134", "21EEE135", "21EEE136", "21MAI141", "21EEE142", "21EEE143", "21EEE144", "21EEE145", "21EEE146"]
    elif faculty_department == "Electrical and Electronics engineering" and selected_semester=="5" or selected_semester=="6":
        subjects = ["20EEE151", "20EEE152", "20EEE153", "20EEE154", "20EEE155", "20EEE161", "20EEE162", "20EEE163", "20EEE164", "20EEE165"]
    elif faculty_department == "Electrical and Electronics engineering" and selected_semester=="7" or selected_semester=="8":
        subjects = ["19EEE171", "19EEE172", "19EEE173", "19EEE174", "19EEE175", "19EEE181", "19EEE182", "19EEE183"]

    elif faculty_department == "Mechanical engineering" and selected_semester=="3" or selected_semester=="4":
        subjects = ["21MAI131", "21ME132", "21ME133", "21ME134", "21ME135", "21ME136", "21MAI141", "21ME142", "21ME143", "21ME144", "21ME145", "21ME146"]
    elif faculty_department == "Mechanical engineering" and selected_semester=="5" or selected_semester=="6":
        subjects = ["20ME151", "20ME152", "20ME153", "20ME154", "20ME155", "20ME161", "20ME162", "20ME163", "20ME164", "20ME165"]
    elif faculty_department == "Mechanical engineering" and selected_semester=="7" or selected_semester=="8":
        subjects = ["19ME171", "19ME172", "19ME173", "19ME174", "19ME175", "19ME181", "19ME182", "19ME183"]
      
    return render(request, 'edu_app/attendance.html', {
        'student_list': student_list,
        'subjects': subjects,
        'selected_subject': selected_subject,
        'selected_semester': selected_semester,
    })

def update_cie(request):
    if request.method=='POST':
        usn = request.POST["usn"]
        username = usn
        Branch = request.POST["Branch"]
        branch = Branch
        semester = request.POST["semester"]
        exist = students.objects.filter(username=username,Branch=Branch,semester=semester).exists()
        if exist:
            if not check_usn_exists(usn):
                obj_new = student_marks.objects.get(usn=usn)
                obj_new.sub_1_code = request.POST["sub_1_code"]
                obj_new.sub_1 = request.POST["sub_1"]
                obj_new.sub_2_code = request.POST["sub_2_code"]
                obj_new.sub_2 = request.POST["sub_2"]
                obj_new.sub_3_code = request.POST["sub_3_code"]
                obj_new.sub_3 = request.POST["sub_3"]
                obj_new.sub_4_code = request.POST["sub_4_code"]
                obj_new.sub_4 = request.POST["sub_4"]
                obj_new.sub_5_code = request.POST["sub_5_code"]
                obj_new.sub_5 = request.POST["sub_5"]
                obj_new.sub_6_code = request.POST["sub_6_code"]
                obj_new.sub_6 = request.POST["sub_6"]
                obj_new.save()
            else:
                sub_1_code = request.POST["sub_1_code"]
                sub_1 = request.POST["sub_1"]
                sub_2_code = request.POST["sub_2_code"]
                sub_2 = request.POST["sub_2"]
                sub_3_code = request.POST["sub_3_code"]
                sub_3 = request.POST["sub_3"]
                sub_4_code = request.POST["sub_4_code"]
                sub_4 = request.POST["sub_4"]
                sub_5_code = request.POST["sub_5_code"]
                sub_5 = request.POST["sub_5"]
                sub_6_code = request.POST["sub_6_code"]
                sub_6 = request.POST["sub_6"]
                obj = student_marks(usn=usn,branch=branch,semester=semester,sub_1_code=sub_1_code,sub_1=sub_1,sub_2_code=sub_2_code,sub_2=sub_2,sub_3_code=sub_3_code,sub_3=sub_3,sub_4_code=sub_4_code,sub_4=sub_4,sub_5_code=sub_5_code,sub_5=sub_5,sub_6_code=sub_6_code,sub_6=sub_6)
                obj.save()
            messages.success(request,"CIE marks updated successfully")
            return redirect('update_cie')
        else:
            messages.success(request,"Make sure that USN, branch and semester match and try again")
            return redirect('update_cie')
    else:
        return render(request,'edu_app/update_cie.html')

def view_attendance(request):
    student_username = request.user.username
    selected_subject = request.GET.get('subject', '') 
    stu_username = request.user.username
    stu = students.objects.get(username=stu_username)
    branch = stu.Branch
    semester=stu.semester
    attendance_data = Stu_Attendance.objects.filter(student_name__username=student_username, subject=selected_subject)
    for entry in attendance_data:
        entry.status = "Present" if entry.is_present else "Absent"
    
    if semester=="1" or semester=="2":
        subjects=["22MAT111", "22CPC112","22CHE113", "22BEC114", "22EGD115","22MAT121", "22PHY122", "22BEE123", "22BES124", "22CPC125"]
    elif branch == "Computer Science and engineering" and semester=="3" or semester=="4":
        subjects = ["21MAI131", "21CSE132", "21CSE133", "21CSE134", "21CSE135", "21CSE136", "21MAI141", "21CSE142", "21CSE143", "21CSE144", "21CSE145", "21CSE146"]
    elif branch == "Computer Science and engineering" and semester=="5" or semester=="6":
        subjects = ["20CSE151", "20CSE152", "20CSE153", "20CSE154", "20CSE155", "20CSE161", "20CSE162", "20CSE163", "20CSE164", "20CSE165"]
    elif branch == "Computer Science and engineering" and semester=="7" or semester=="8":
        subjects = ["19CSE171", "19CSE172", "19CSE173", "19CSE174", "19CSE175", "19CSE181", "19CSE182", "19CSE183"]
        
    elif branch == "Infromation Science and Engineering" and semester=="3" or semester=="4":
        subjects = ["21MAI131", "21ISE132", "21ISE133", "21ISE134", "21ISE135", "21ISE136", "21MAI141", "21ISE142", "21ISE143", "21ISE144", "21ISE145", "21ISE146"]
    elif branch == "Infromation Science and Engineering" and semester=="5" or semester=="6":
        subjects = ["20ISE151", "20ISE152", "20ISE153", "20ISE154", "20ISE155", "20ISE161", "20ISE162", "20ISE163", "20ISE164", "20ISE165"]
    elif branch == "Infromation Science and Engineering" and semester=="7" or semester=="8":
        subjects = ["19ISE171", "19ISE172", "19ISE173", "19ISE174", "19ISE175", "19ISE181", "19ISE182", "19ISE183"]
        
    elif branch == "Artifical Intelligence and machine learning" and semester=="3" or semester=="4":
        subjects = ["21MAI131", "21AIML132", "21AIML133", "21AIML134", "21AIML135", "21AIML136", "21MAI141", "21AIML142", "21AIML143", "21AIML144", "21AIML145", "21AIML146"]
    elif branch == "Artifical Intelligence and machine learning" and semester=="5" or semester=="6":
        subjects = ["20AIML151", "20AIML152", "20AIML153", "20AIML154", "20AIML155", "20AIML161", "20AIML162", "20AIML163", "20AIML164", "20AIML165"]
    elif branch == "Artifical Intelligence and machine learning" and semester=="7" or semester=="8":
        subjects = ["19AIML171", "19AIML172", "19AIML173", "19AIML174", "19AIML175", "19AIML181", "19AIML182", "19AIML183"]

    elif branch == "Electronics and Communication Engineering" and semester=="3" or semester=="4":
        subjects = ["21MAI131", "21ECE132", "21ECE133", "21ECE134", "21ECE135", "21ECE136", "21MAI141", "21ECE142", "21ECE143", "21ECE144", "21ECE145", "21ECE146"]
    elif branch == "Electronics and Communication Engineering" and semester=="5" or semester=="6":
        subjects = ["20ECE151", "20ECE152", "20ECE153", "20ECE154", "20ECE155", "20ECE161", "20ECE162", "20ECE163", "20ECE164", "20ECE165"]
    elif branch == "Electronics and Communication Engineering" and semester=="7" or semester=="8":
        subjects = ["19ECE171", "19ECE172", "19ECE173", "19ECE174", "19ECE175", "19ECE181", "19ECE182", "19ECE183"]
    
    elif branch == "Electrical and Electronics engineering" and semester=="3" or semester=="4":
        subjects = ["21MAI131", "21EEE132", "21EEE133", "21EEE134", "21EEE135", "21EEE136", "21MAI141", "21EEE142", "21EEE143", "21EEE144", "21EEE145", "21EEE146"]
    elif branch == "Electrical and Electronics engineering" and semester=="5" or semester=="6":
        subjects = ["20EEE151", "20EEE152", "20EEE153", "20EEE154", "20EEE155", "20EEE161", "20EEE162", "20EEE163", "20EEE164", "20EEE165"]
    elif branch == "Electrical and Electronics engineering" and semester=="7" or semester=="8":
        subjects = ["19EEE171", "19EEE172", "19EEE173", "19EEE174", "19EEE175", "19EEE181", "19EEE182", "19EEE183"]

    elif branch == "Mechanical engineering" and semester=="3" or semester=="4":
        subjects = ["21MAI131", "21ME132", "21ME133", "21ME134", "21ME135", "21ME136", "21MAI141", "21ME142", "21ME143", "21ME144", "21ME145", "21ME146"]
    elif branch == "Mechanical engineering" and semester=="5" or semester=="6":
        subjects = ["20ME151", "20ME152", "20ME153", "20ME154", "20ME155", "20ME161", "20ME162", "20ME163", "20ME164", "20ME165"]
    elif branch == "Mechanical engineering" and semester=="7" or semester=="8":
        subjects = ["19ME171", "19ME172", "19ME173", "19ME174", "19ME175", "19ME181", "19ME182", "19ME183"]

    return render(request, 'edu_app/view_attendance.html', {'attendance_data': attendance_data, 'subjects': subjects, 'selected_subject': selected_subject})


def notification(request):
    sem=fa_update_notification.objects.all()
    return render(request, 'edu_app/notifications.html', {'sem':sem})

def view_complaints(request):
    comp=stu_complaints.objects.all()
    return render(request,'edu_app/view_complaints.html',{'comp':comp})

    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('landing'))



