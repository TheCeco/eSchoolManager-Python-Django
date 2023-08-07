from django.urls import path

from eSchoolManager.principal_app.views.classes_views import AssignTeacher
from eSchoolManager.principal_app.views.principal_profile_views import principal_details_view, EditPrincipalProfile
from eSchoolManager.principal_app.views.students_views import get_all_students
from eSchoolManager.principal_app.views.teachers_views import get_all_teachers, assign_subjects_to_teacher, \
    edit_subject, delete_teacher_subject
from eSchoolManager.principal_app.views.users_views import approve_user, pending_users, DeleteUser


urlpatterns = [
    path('details/', principal_details_view, name='principal_details'),
    path('details/edit/<int:pk>', EditPrincipalProfile.as_view(), name='edit_profile'),
    path('approve_user/<int:pk>', approve_user, name='approve_user'),
    path('pending_users/', pending_users, name='pending_users'),
    path('teachers/', get_all_teachers, name='teachers_view'),
    path('teachers/teacher_detail/assign_subjects/<int:pk>', assign_subjects_to_teacher, name='assign_subject'),
    path('teachers/teacher_detail/edit_subjects/<int:teacher_id>/<int:subject_id>', edit_subject, name='edit_subject'),
    path('teachers/teacher_detail/delete_subjects/<int:teacher_id>/<int:subject_id>',
         delete_teacher_subject, name='delete_subject'),
    path('students/', get_all_students, name='students_view'),
    path('users/<int:pk>', DeleteUser.as_view(), name='delete_users'),
    path('classes/assign_teacher/', AssignTeacher.as_view(), name='assign_teacher'),
]
