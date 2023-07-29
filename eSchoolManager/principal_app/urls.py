from django.urls import path

from eSchoolManager.principal_app.views import approve_user, pending_users, assign_subjects_to_teacher, UserTypesView, \
    edit_subject, delete_teacher_subject, principal_details_view, EditPrincipalProfile, DeleteTeacher, AssignTeacher

urlpatterns = [
    path('details/', principal_details_view, name='principal_details'),
    path('details/edit/<int:pk>', EditPrincipalProfile.as_view(), name='edit_profile'),
    path('approve_user/<int:pk>', approve_user, name='approve_user'),
    path('pending_users/', pending_users, name='pending_users'),
    path('<str:user_type>/', UserTypesView.as_view(), name='types_view'),
    path('teachers/teacher_detail/assign_subjects/<int:pk>', assign_subjects_to_teacher, name='assign_subject'),
    path('teachers/teacher_detail/edit_subjects/<int:teacher_id>/<int:subject_id>', edit_subject, name='edit_subject'),
    path('teachers/teacher_detail/delete_subjects/<int:teacher_id>/<int:subject_id>',
         delete_teacher_subject, name='delete_subject'),
    path('users/<int:pk>', DeleteTeacher.as_view(), name='delete_users'),
    path('classes/assign_teacher/', AssignTeacher.as_view(), name='assign_teacher'),
]
