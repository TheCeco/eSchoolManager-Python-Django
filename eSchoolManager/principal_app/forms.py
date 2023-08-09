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
    school_class = forms.ModelChoiceField(queryset=ClassesModel.objects.all(), required=False, widget=forms.Select)

    class Meta:
        model = UserModel
        fields = ['email', 'first_name', 'last_name', 'user_type', 'school_class']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        self.fields['first_name'].disabled = True
        self.fields['last_name'].disabled = True
        self.fields['user_type'].widget.attrs.update({
            'class': 'form-control',
            'type': 'choice'})
        self.fields['school_class'].widget.attrs.update({
            'class': 'form-control',
            'type': 'choice'
        })


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
        widgets = {
            'teacher': forms.Select(attrs={
                'class': 'form-control'
            }),
            'school_class': forms.Select(attrs={
                'class': 'form-control'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'teacher': 'Teacher Name:',
            'subject': 'Subject Name:',
            'school_class': 'Class:'
        }
        error_messages = {

        }


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
