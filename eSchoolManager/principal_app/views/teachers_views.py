from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic as views

from eSchoolManager.classes_app.models import TeacherClass
from eSchoolManager.common_app.forms import SearchForm
from eSchoolManager.principal_app.forms import EditTeacherSubject, AssignSubjectsToTeachersForm
from eSchoolManager.principal_app.models import TeacherSubjects
from eSchoolManager.principal_app.tasks import remove_teacher_from_classes
from eSchoolManager.teachers_app.models import TeacherProfile

UserModel = get_user_model()


@login_required
@permission_required('principal_app.view_teachersubjects', raise_exception=True)
def get_all_teachers(request):
    teachers = TeacherProfile.objects.all()
    search_form = SearchForm()
    search_query = request.GET.get('search', '')

    if request.method == 'POST':
        search_form = SearchForm(request.POST)

        if search_form.is_valid():
            search_query = search_form.cleaned_data['search_query']
            teachers = teachers.filter(user__first_name__icontains=search_query) \
                       or teachers.filter(user__last_name__icontains=search_query)

    else:
        teachers = teachers.filter(user__first_name__icontains=search_query) \
                   or teachers.filter(user__last_name__icontains=search_query)

    paginator = Paginator(teachers, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'search_query': search_query
    }

    return render(request, 'principal_templates/teachers/teachers_template.html', context=context)


@login_required
@permission_required('principal_app.add_teachersubjects', raise_exception=True)
def assign_subjects_to_teacher(request, pk):
    teacher = get_object_or_404(TeacherProfile, pk=pk)

    initial_data = {
        'teacher': teacher
    }

    form = AssignSubjectsToTeachersForm(request.POST or None, initial=initial_data)

    if form.is_valid():
        form.save()

        return redirect('teacher_details', pk=teacher.user_id)

    context = {
        'teacher': teacher,
        'form': form
    }

    return render(request, 'principal_templates/teachers/assign_subject.html', context=context)


@login_required
@permission_required('principal_app.change_teachersubjects', raise_exception=True)
def edit_subject(request, teacher_id, subject_id):
    teacher = get_object_or_404(TeacherProfile, pk=teacher_id)
    teacher_subject = get_object_or_404(TeacherSubjects, teacher=teacher, subject_id=subject_id)
    form = EditTeacherSubject(request.POST or None, instance=teacher_subject)

    if form.is_valid():
        teacher_subject.teacher = form.cleaned_data['teacher']
        teacher_subject.subject = form.cleaned_data['subject']
        form.save()
        return redirect('teacher_details', pk=teacher.user_id)

    context = {
        'teacher_id': teacher_id,
        'subject_id': subject_id,
        'form': form
    }

    return render(request, 'principal_templates/teachers/edit_teacher_subject.html', context=context)


@login_required
@permission_required('principal_app.delete_teachersubjects', raise_exception=True)
def delete_teacher_subject(request, teacher_id, subject_id):
    teacher = get_object_or_404(TeacherProfile, pk=teacher_id)
    subject = get_object_or_404(TeacherSubjects, teacher=teacher, subject_id=subject_id)
    teacher_classes = TeacherClass.objects.filter(teacher=teacher, subject_id=subject_id)
    subject.delete()
    remove_teacher_from_classes(teacher_classes)
    return redirect('teacher_details', pk=teacher.user_id)


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required({
    'teachers_app.delete_teacherprofile',
    'students_app.delete_studentprofile',
    'accounts_app.delete_schooluser'
}, raise_exception=True), name='dispatch')
class DeleteTeacher(views.DeleteView):
    template_name = 'principal_templates/teachers/delete_teachers.html'
    success_url = reverse_lazy('teachers_view')

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(UserModel, pk=pk)

    def delete(self, request, *args, **kwargs):
        teacher = self.get_object()
        teacher.delete()
        return self.success_url
