from django import forms

from eSchoolManager.students_app.models import AddGradeToStudentModel
from eSchoolManager.teachers_app.models import TeacherProfile
from eSchoolManager.students_app.validators import CheckIfValidPhone


class EditTeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'image_url': forms.URLInput(attrs={
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }


class GradeToStudentForm(forms.ModelForm):
    class Meta:
        model = AddGradeToStudentModel
        fields = '__all__'
        widgets = {
            'grade': forms.Select(attrs={
                'class': 'form-control'
            }),
            'student': forms.Select(attrs={
                'class': 'form-control'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].disabled = True
        self.fields['subject'].disabled = True
