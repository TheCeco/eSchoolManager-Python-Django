from django.contrib.auth.decorators import permission_required, login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404

from eSchoolManager.common_app.forms import SearchForm
from eSchoolManager.students_app.models import StudentProfile


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
            students = get_list_or_404(students, user__first_name__icontains=search_query) \
                       or get_list_or_404(students, user__last_name__icontains=search_query)

    else:
        students = get_list_or_404(students, user__first_name__icontains=search_query) \
                       or get_list_or_404(students, user__last_name__icontains=search_query)

    paginator = Paginator(students, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'search_query': search_query
    }

    return render(request, 'principal_templates/students/students_template.html', context=context)
