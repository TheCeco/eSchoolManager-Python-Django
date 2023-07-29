from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic as views

from .controller import check_user_type
from .models import TeacherSubjects, PrincipalProfile
from .forms import ApproveUsers, AssignSubjectsToTeachersForm, EditTeacherSubject, EditPrincipalProfileForm, \
    AssignClassToTeacherForm
from ..students_app.models import StudentProfile
from ..classes_app.models import ClassesModel, TeacherClass
from ..teachers_app.models import TeacherProfile
from ..accounts_app.forms import SchoolUserEditForm

UserModel = get_user_model()


# Create your views here.
@login_required
@permission_required({
    'accounts_app.view_schooluser',
    'principal_app.view_principalprofile'
}, raise_exception=True)
def principal_details_view(request):
    pk = request.user.pk
    profile = PrincipalProfile.objects.get(user_id=pk)

    context = {
        'profile': profile
    }

    return render(request, 'principal_templates/profile/details_principal_profile.html', context=context)


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required({
    'principal_app.change_principalprofile',
    'accounts_app.change_schooluser'},
    raise_exception=True), name='dispatch')
class EditPrincipalProfile(views.UpdateView):
    template_name = 'principal_templates/profile/edit_principal_profile.html'
    form_class = SchoolUserEditForm
    form_class2 = EditPrincipalProfileForm

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = UserModel.objects.get(pk=pk)

        if obj.groups.first().name == 'Principal':
            return obj
        raise Http404("You don't have permission to edit this profile.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['p_form'] = self.form_class2(instance=self.request.user.principalprofile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        p_form = self.form_class2(request.POST, instance=self.request.user.principalprofile)

        if form.is_valid() and p_form.is_valid():
            return self.form_valid(form, p_form)
        else:
            return self.form_invalid(form, p_form)

    def form_valid(self, form, p_form):
        form.save()
        p_form.save()
        return redirect('principal_details')

    def form_invalid(self, form, p_form):
        return self.render_to_response(self.get_context_data(form=form, p_form=p_form))


@login_required
@permission_required(
    {
        'accounts_app.add_schooluser',
        'students_app.add_studentprofile',
        'teachers_app.add_teacherprofile'
    }
    , raise_exception=True)
def pending_users(request):  # TODO: Can be a CBV
    users = UserModel.objects.filter(is_active=False)

    context = {
        'users': users
    }

    return render(request, 'principal_templates/users/pending_users.html', context=context)


@login_required
@permission_required(
    {
        'accounts_app.add_schooluser',
        'students_app.add_studentprofile',
        'teachers_app.add_teacherprofile'
    }, raise_exception=True
)
def approve_user(request, pk):
    user = UserModel.objects.get(pk=pk)
    form = ApproveUsers(request.POST or None, instance=user)

    if form.is_valid():
        if 'approve' in request.POST:
            user.is_active = True
            user.is_staff = True
            form.save()

            check_user_type(form, pk)
            return redirect('pending_users')
        elif 'delete' in request.POST:
            user.delete()
            return redirect('pending_users')

    context = {
        'user': user,
        'form': form
    }

    return render(request, 'principal_templates/users/approve_user.html', context=context)


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('principal_app.view_teachersubjects', raise_exception=True), name='dispatch')
class UserTypesView(views.ListView):
    def get_queryset(self):
        user_type = self.kwargs.get('user_type')
        if user_type == 'teachers':
            return TeacherProfile.objects.all()
        elif user_type == 'students':
            return StudentProfile.objects.all()
        else:
            return Http404('No such user type!')

    def get_template_names(self):
        user_type = self.kwargs.get('user_type')
        if user_type == 'teachers':
            return 'principal_templates/teachers/teachers_template.html'
        elif user_type == 'students':
            return 'principal_templates/students/students_template.html'
        else:
            return Http404('No such user type!')


@login_required
@permission_required('principal_app.add_teachersubjects', raise_exception=True)
def assign_subjects_to_teacher(request, pk):
    teacher = TeacherProfile.objects.get(pk=pk)

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
    teacher = TeacherProfile.objects.get(pk=teacher_id)
    teacher_subject = TeacherSubjects.objects.get(teacher=teacher, subject_id=subject_id)
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
    teacher = TeacherProfile.objects.get(pk=teacher_id)
    subject = TeacherSubjects.objects.get(subject_id=subject_id, teacher=teacher)
    subject.delete()
    return redirect('teacher_details', pk=teacher.user_id)


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required({
    'teachers_app.delete_teacherprofile',
    'accounts_app.delete_schooluser'
}, raise_exception=True), name='dispatch')
class DeleteTeacher(views.DeleteView):
    template_name = 'principal_templates/users/delete_users.html'
    model = TeacherProfile
    success_url = reverse_lazy('types_view', kwargs={'user_type': 'teachers'})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return UserModel.objects.get(pk=pk)

    def delete(self, request, *args, **kwargs):
        teacher = self.get_object()
        teacher.delete()
        return redirect(self.success_url)


class AssignTeacher(views.CreateView):
    form_class = AssignClassToTeacherForm
    template_name = 'principal_templates/assign_teacher.html'
    success_url = reverse_lazy('classes_list')

