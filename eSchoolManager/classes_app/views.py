from django.shortcuts import render
from django.views import generic as views

from eSchoolManager.classes_app.models import ClassesModel, TeacherClass
from eSchoolManager.students_app.models import StudentProfile


# Create your views here.
class ClassesList(views.ListView):
    template_name = 'classes_templates/classes_template.html'
    model = ClassesModel


class ClassDetailsView(views.DetailView):
    template_name = 'classes_templates/class_details.html'

    def get_context_data(self, **kwargs):
        class_value = self.get_object()
        teacher_class = TeacherClass.objects.filter(school_class=class_value)
        student_class = StudentProfile.objects.filter(school_class=class_value)

        context = super().get_context_data(**kwargs)
        context['teachers'] = teacher_class
        context['students'] = student_class

        return context

    def get_object(self, queryset=None):
        class_id = self.kwargs.get('pk')
        return ClassesModel.objects.get(pk=class_id)