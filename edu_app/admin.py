from django.contrib import admin
from edu_app.models import faculty_info,students,student_marks,fa_update_notification,stu_complaints,Stu_Attendance,payments
# Register your models here.

admin.site.register(faculty_info)
admin.site.register(students)
admin.site.register(student_marks)
admin.site.register(fa_update_notification)
admin.site.register(stu_complaints)
admin.site.register(Stu_Attendance)
admin.site.register(payments)