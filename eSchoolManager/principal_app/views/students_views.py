from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required, login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic as views

from eSchoolManager.common_app.forms import SearchForm
from eSchoolManager.students_app.models import StudentProfile

UserModel = get_user_model()

@login_required
@permission_required('students_app.view_studentprofile', raise_exception=True)
def get_all_students(request):
    students = StudentProfile.objects.all()
    search_form = SearchForm()
    search_query = request.GET.get('search', '')

    if request.method == 'POST':
        search_form = SearchForm(request.POST)

        if search_form.is_valid():
            search_query = search_form.cleaned_data['search_query']
            students = students.filter(user__first_name__icontains=search_query) \
                       or students.filter(user__last_name__icontains=search_query)

    else:
        students = students.filter(user__first_name__icontains=search_query) \
                       or students.filter(user__last_name__icontains=search_query)

    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'search_query': search_query
    }

    return render(request, 'principal_templates/students/students_template.html', context=context)

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required({
    'teachers_app.delete_teacherprofile',
    'students_app.delete_studentprofile',
    'accounts_app.delete_schooluser'
}, raise_exception=True), name='dispatch')
class DeleteStudent(views.DeleteView):
    template_name = 'principal_templates/students/delete_students.html'
    success_url = reverse_lazy('students_view')

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(UserModel, pk=pk)

    def delete(self, request, *args, **kwargs):
        teacher = self.get_object()
        teacher.delete()
        return self.success_url
