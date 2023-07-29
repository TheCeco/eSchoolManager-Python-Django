from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from eSchoolManager.students_app.models import StudentProfile
from eSchoolManager.teachers_app.models import TeacherProfile

UserModel = get_user_model()


def check_user_type(form, pk):
    cleaned_data = form.cleaned_data['user_type']

    if cleaned_data == 'teacher':
        return create_user_profile('teacher', form, pk)
    return create_user_profile('student', form, pk)


def create_user_profile(user_type, form, pk):
    if user_type == 'student':
        school_class = form.cleaned_data['school_class']
        student = StudentProfile(user_id=pk, school_class=school_class)
        student.save()
    else:
        teacher = TeacherProfile(user_id=pk)
        teacher.save()
    add_user_to_group(user_type, pk)


def add_user_to_group(user_type, pk):
    try:
        group_name = user_type.capitalize()
        user = UserModel.objects.get(pk=pk)
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        return True, f'{user.get_full_name()} added to a group {group_name} successfully'
    except UserModel.DoesNotExist:
        return False, "User not found."
    except Group.DoesNotExist:
        return False, "Group not found."
