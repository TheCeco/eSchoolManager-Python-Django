from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.utils.decorators import method_decorator
from django.views import generic as views

from eSchoolManager.accounts_app.forms import SchoolUserEditForm
from eSchoolManager.common_app.models import SubjectsModel
from eSchoolManager.mixins.user_details_mixins import UserProfileDetailsMixin
from eSchoolManager.students_app.forms import EditStudentProfileForm
from eSchoolManager.students_app.models import StudentProfile, AddGradeToStudentModel

UserModel = get_user_model()


# Create your views here.
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required({
    'students_app.view_studentprofile',
    'accounts_app.view_schooluser'
}, raise_exception=True), name='dispatch')
class StudentDetailsView(UserProfileDetailsMixin):
    template_name = 'students_templates/student_details.html'
    profile = StudentProfile


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
        obj = get_object_or_404(UserModel, pk=self.request.user.pk)

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
        return redirect('student_details', pk=self.request.user.pk)

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
        try:
            user_id = pk if pk == self.request.user.pk else self.request.user.pk
            return get_object_or_404(UserModel, pk=user_id)
        except:
            return get_object_or_404(UserModel, pk=pk)

    def get_context_data(self, **kwargs):
        subjects = SubjectsModel.objects.all()
        student = get_object_or_404(StudentProfile, user=self.get_object())
        student_grades = AddGradeToStudentModel.objects.filter(student=student)

        context = super().get_context_data(**kwargs)
        context['subjects'] = subjects
        context['student_grades'] = student_grades
        context['average_grades'] = self.get_average_grades(student_grades)

        return context

    def get_average_grades(self, student_grades):
        average_grades = {}
        for data in student_grades:
            # Check if subject in dict if not add it
            if data.subject not in average_grades:
                average_grades[data.subject] = 0

            # Adding the grade to the subject
            average_grades[data.subject] += data.grade.grade

        # Calculating the sum of the grades per subject to average grade
        for subject, grade in average_grades.items():
            all_subject_grades = get_list_or_404(student_grades, subject=subject)
            average_grades[subject] = grade / len(all_subject_grades)

        return average_grades
