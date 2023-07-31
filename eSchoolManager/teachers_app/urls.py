from django.urls import path

from .views import TeacherDetailsView, EditTeacherProfile, TeacherClasses, TeacherGradesTables, EditStudentGrade, \
    AddGrade

urlpatterns = [
    path('details/<int:pk>', TeacherDetailsView.as_view(), name='teacher_details'),
    path('edit/<int:pk>', EditTeacherProfile.as_view(), name='teacher_edit'),
    path('classes/', TeacherClasses.as_view(), name='teacher_classes'),
    path('classes/<int:class_id>', TeacherGradesTables.as_view(), name='students_in_class'),
    path('grades/edit/<int:pk>', EditStudentGrade.as_view(), name='edit_student_grade'),
    path('grades/add/<int:student_id>/<int:subject_id>', AddGrade.as_view(), name='add_grade')
]
