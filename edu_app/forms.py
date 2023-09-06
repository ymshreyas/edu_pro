from django import forms
from edu_app.models import faculty_info


class Facultyprofileinfoforms(forms.ModelForm):
    class Meta():
        model = faculty_info
        fields = ('username','email','password','profile_pic','department','name','Designation','specialisation','DOJ','years_of_experience','bachelor_degree','bachelor_instituition','bachelor_year','Masters_degree','Masters_instituition','Masters_year','Phd','Phd_instituition','Phd_year',)