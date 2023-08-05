from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic as views

from eSchoolManager.classes_app.models import ClassesModel, TeacherClass
from eSchoolManager.students_app.models import StudentProfile


# Create your views here.
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required({
    'classes_app.view_classesmodel'
}, raise_exception=True), name='dispatch')
class ClassesList(views.ListView):
    template_name = 'classes_templates/classes_template.html'
    model = ClassesModel


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required({
    'classes_app.view_classesmodel'
}, raise_exception=True), name='dispatch')
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
        return get_object_or_404(ClassesModel, pk=class_id)
