from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic as views

from eSchoolManager.principal_app.forms import AssignClassToTeacherForm


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required({
    'classes_app.add_teacherclass'
}, raise_exception=True), name='dispatch')
class AssignTeacher(views.CreateView):
    form_class = AssignClassToTeacherForm
    template_name = 'principal_templates/classes/assign_teacher.html'
    success_url = reverse_lazy('classes_list')
