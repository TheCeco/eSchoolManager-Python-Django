from django.urls import path

from .views import StudentDetailsView, GradesDetailsView, EditStudentProfileView

urlpatterns = [
    path('details/<int:pk>', StudentDetailsView.as_view(), name='student_details'),
    path('grades/<int:pk>', GradesDetailsView.as_view(), name='student_grades'),
    path('edit/<int:pk>', EditStudentProfileView.as_view(), name='student_edit')
]
