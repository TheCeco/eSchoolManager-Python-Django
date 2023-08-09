from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic as views

from eSchoolManager.principal_app.forms import AssignClassToTeacherForm
from eSchoolManager.principal_app.models import TeacherSubjects
from eSchoolManager.teachers_app.models import TeacherProfile


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required({
    'classes_app.add_teacherclass'
}, raise_exception=True), name='dispatch')
class AssignTeacher(views.CreateView):
    form_class = AssignClassToTeacherForm
    template_name = 'principal_templates/classes/assign_teacher.html'
    success_url = reverse_lazy('classes_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers_subject'] = self.get_teachers_subjects()
        return context

    def get_teachers_subjects(self):
        teachers_subjects = TeacherSubjects.objects.all()
        teachers_subjects_data = []

        for obj in teachers_subjects:
            teachers_subjects_data.append({
                obj.teacher_id: obj.subject.subject_name,
            })

        return teachers_subjects_data
