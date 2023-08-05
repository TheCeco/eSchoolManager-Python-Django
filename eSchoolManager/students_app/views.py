from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import generic as views

from eSchoolManager.accounts_app.forms import SchoolUserEditForm
from eSchoolManager.common_app.models import SubjectsModel
from eSchoolManager.students_app.forms import EditStudentProfileForm
from eSchoolManager.students_app.models import StudentProfile, AddGradeToStudentModel

UserModel = get_user_model()


# Create your views here.
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required({
    'students_app.view_studentprofile',
    'accounts_app.view_schooluser'
}, raise_exception=True), name='dispatch')
class StudentDetailsView(views.DetailView):
    template_name = 'students_templates/student_details.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        user_id = pk if pk else self.request.user.pk
        return StudentProfile.objects.get(user_id=user_id)


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required({
    'students_app.change_studentprofile',
    'accounts_app.change_schooluser'
}, raise_exception=True), name='dispatch')
class EditStudentProfileView(views.UpdateView):
    template_name = 'students_templates/student_edit.html'
    form_class = SchoolUserEditForm
    form_class2 = EditStudentProfileForm

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        obj = UserModel.objects.get(pk=pk)

        if obj.groups.first().name == 'Student':
            return obj
        raise Http404("You don't have permission to edit this profile.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['p_form'] = self.form_class2(instance=self.request.user.studentprofile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        p_form = self.form_class2(request.POST, instance=self.request.user.studentprofile)

        if form.is_valid() and p_form.is_valid():
            return self.form_valid(form, p_form)
        else:
            return self.form_invalid(form, p_form)

    def form_valid(self, form, p_form):
        form.save()
        p_form.save()
        return redirect('student_details', pk=self.kwargs.get('pk'))

    def form_invalid(self, form, p_form):
        return self.render_to_response(self.get_context_data(form=form, p_form=p_form))


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required({
    'students_app.view_addgradetostudentmodel'
}, raise_exception=True), name='dispatch')
class GradesDetailsView(views.DetailView):
    template_name = 'students_templates/student_grades.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return UserModel.objects.get(pk=pk)

    def get_context_data(self, **kwargs):
        subjects = SubjectsModel.objects.all()
        student = StudentProfile.objects.get(user=self.get_object())
        student_grades = AddGradeToStudentModel.objects.filter(student=student)

        context = super().get_context_data(**kwargs)
        context['subjects'] = subjects
        context['student_grades'] = student_grades
        context['average_grades'] = self.get_average_grades(student_grades)

        return context

    def get_average_grades(self, student_grades):
        average_grades = {}
        for data in student_grades:
            if data.subject not in average_grades:
                average_grades[data.subject] = 0

            average_grades[data.subject] += data.grade.grade

        for subject, grade in average_grades.items():
            all_subject_grades = student_grades.filter(subject=subject)
            average_grades[subject] = grade / len(all_subject_grades)

        print(average_grades.items())
        return average_grades
