from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import generic as views

from .forms import EditTeacherProfileForm, GradeToStudentForm
from .models import TeacherProfile
from ..accounts_app.forms import SchoolUserEditForm
from ..classes_app.models import TeacherClass
from ..common_app.models import SubjectsModel
from ..principal_app.models import TeacherSubjects
from ..students_app.models import StudentProfile, AddGradeToStudentModel

UserModel = get_user_model()


class TeacherDetailsView(views.DetailView):
    template_name = 'teachers_templates/teacher_details.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        user_id = pk if pk else self.request.user.pk
        return TeacherProfile.objects.get(user_id=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher_subjects'] = TeacherSubjects.objects.filter(teacher=self.get_object())
        context['classes'] = TeacherClass.objects.filter(teacher=self.get_object())

        print(context['classes'])

        return context


class EditTeacherProfile(views.UpdateView):
    template_name = 'teachers_templates/teacher_edit.html'
    form_class = SchoolUserEditForm
    form_class2 = EditTeacherProfileForm

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        obj = UserModel.objects.get(pk=pk)

        if obj.groups.first().name == 'Teacher':
            return obj
        raise Http404("You don't have permission to edit this profile.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['p_form'] = self.form_class2(instance=self.request.user.teacherprofile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        p_form = self.form_class2(request.POST, instance=self.request.user.teacherprofile)

        if form.is_valid() and p_form.is_valid():
            return self.form_valid(form, p_form)
        else:
            return self.form_invalid(form, p_form)

    def form_valid(self, form, p_form):
        form.save()
        p_form.save()
        return redirect('teacher_details', pk=self.kwargs.get('pk'))

    def form_invalid(self, form, p_form):
        return self.render_to_response(self.get_context_data(form=form, p_form=p_form))


class TeacherClasses(views.ListView):
    template_name = 'teachers_templates/teacher_classes.html'
    model = TeacherClass

    def get_queryset(self):
        teacher = self.request.user.teacherprofile
        return TeacherClass.objects.filter(teacher_id=teacher.pk)


class TeacherGradesTables(views.DetailView):
    template_name = 'teachers_templates/students_in_class.html'

    def get_object(self, queryset=None):
        class_id = self.kwargs.get('class_id')
        return StudentProfile.objects.filter(school_class_id=class_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.request.user.pk
        teacher = TeacherProfile.objects.get(user_id=pk)
        student_subjects = AddGradeToStudentModel.objects.all()
        context['teacher'] = teacher
        context['student_subjects'] = student_subjects
        context['average_grades'] = self.get_average_grades_for_subject(teacher, student_subjects, self.get_object())
        return context

    def get_average_grades_for_subject(self, teacher, student_subjects, students):
        average_grades = {}

        for subject in teacher.teachersubjects_set.all():
            for student in student_subjects:
                if student.subject.subject_name == subject.subject.subject_name and student.student in students:
                    if student.subject not in average_grades:
                        average_grades[student.subject] = {}

                    if student.student not in average_grades[student.subject]:
                        average_grades[student.subject][student.student] = 0
                    average_grades[student.subject][
                        student.student] += student.grade.grade

        for subject, students in average_grades.items():
            for student, grade_sum in students.items():
                grades = student_subjects.filter(student=student, subject=subject)
                average_grade = grade_sum / len(grades)
                average_grades[subject][student] = average_grade

        return average_grades


class EditStudentGrade(views.UpdateView):
    template_name = 'teachers_templates/edit_student_grade.html'
    form_class = GradeToStudentForm

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return AddGradeToStudentModel.objects.get(pk=pk)

    def form_valid(self, form):
        class_id = self.get_object().student.school_class.pk
        if self.request.POST.get('action') == 'Edit Grade':
            form.save()
        elif self.request.POST.get('action') == 'Delete Grade':
            self.get_object().delete()
        return self.get_success_url(class_id)

    def get_success_url(self, class_id):
        return redirect('students_in_class', class_id=class_id)


class AddGrade(views.CreateView):
    form_class = GradeToStudentForm
    template_name = 'teachers_templates/add_grade.html'

    def get_object(self, queryset=None):
        student_id = self.kwargs.get('student_id')
        subject_id = self.kwargs.get('subject_id')
        student = StudentProfile.objects.get(pk=student_id)
        subject = SubjectsModel.objects.get(pk=subject_id)
        return [student, subject]

    def get_initial(self):
        initial = super().get_initial()
        initial['student'] = self.get_object()[0]
        initial['subject'] = self.get_object()[1]
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.get_object()[0]
        context['subject'] = self.get_object()[1]
        return context

    def form_valid(self, form):
        form.save()
        return self.get_success_url()

    def get_success_url(self):
        student_class_id = self.get_object()[0].school_class.pk
        return redirect('students_in_class', class_id=student_class_id)
