from django import forms
from django.contrib.auth import get_user_model

from .models import TeacherSubjects, PrincipalProfile
from ..classes_app.models import TeacherClass
from ..classes_app.models import ClassesModel

UserModel = get_user_model()


class ApproveUsers(forms.ModelForm):
    USER_TYPES = (
        ('teacher', 'Teacher'),
        ('student', 'Student')
    )

    user_type = forms.ChoiceField(choices=USER_TYPES)
    school_class = forms.ModelChoiceField(queryset=ClassesModel.objects.all(), required=False)

    class Meta:
        model = UserModel
        fields = ['email', 'first_name', 'last_name', 'user_type', 'school_class']


class AssignSubjectsToTeachersForm(forms.ModelForm):
    class Meta:
        model = TeacherSubjects
        fields = '__all__'
        labels = {
            'teacher': 'Teacher: ',
            'subject': 'Subject: '
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].disabled = True


class AssignClassToTeacherForm(forms.ModelForm):
    class Meta:
        model = TeacherClass
        fields = '__all__'


class EditTeacherSubject(AssignSubjectsToTeachersForm):
    pass


class EditPrincipalProfileForm(forms.ModelForm):
    class Meta:
        model = PrincipalProfile
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
