from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic as views

from eSchoolManager.common_app.forms import SearchForm
from eSchoolManager.principal_app.controller import check_user_type
from eSchoolManager.principal_app.forms import ApproveUsers
from eSchoolManager.teachers_app.models import TeacherProfile

UserModel = get_user_model()


@login_required
@permission_required(
    {
        'accounts_app.add_schooluser',
        'students_app.add_studentprofile',
        'teachers_app.add_teacherprofile'
    }
    , raise_exception=True)
def pending_users(request):
    users = UserModel.objects.filter(is_staff=False)
    search_form = SearchForm()
    search_query = request.GET.get('search', '')

    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_query = search_form.cleaned_data['search_query']
            users = get_list_or_404(users, email__icontains=search_query)
    else:
        users = get_list_or_404(users, email__icontains=search_query)

    paginator = Paginator(users, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'users': users,
        'page_obj': page_obj,
        'search_form': search_form,
        'search_query': search_query
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
    user = get_object_or_404(UserModel, pk=pk)
    form = ApproveUsers(request.POST or None, instance=user)

    if form.is_valid():
        if 'approve' in request.POST:
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


