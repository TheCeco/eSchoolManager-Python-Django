from django import forms

from eSchoolManager.students_app.models import StudentProfile


class EditStudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = '__all__'
        exclude = ['school_class', 'user']
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
