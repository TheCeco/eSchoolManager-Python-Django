from django.contrib.auth import views as auth_views, get_user_model
from django.shortcuts import redirect
from django.views import generic as views
from django.urls import reverse_lazy

from eSchoolManager.accounts_app.forms import SchoolUserRegistrationForm, SchoolUserLoginForm

UserModel = get_user_model()


# Create your views here.
class SchoolUserLoginView(auth_views.LoginView):
    template_name = 'accounts_templates/login.html'
    form_class = SchoolUserLoginForm

    def form_invalid(self, form):
        new_user = form.cleaned_data
        users = UserModel.objects.all().values()
        for user in users:
            if user['email'] == new_user['username']:
                return redirect('not_approved')
        return super().form_invalid(form)


class SchoolUserRegisterView(views.CreateView):
    form_class = SchoolUserRegistrationForm
    template_name = 'accounts_templates/register.html'
    success_url = reverse_lazy('not_approved')


class SchoolUserLogoutView(auth_views.LogoutView):
    pass
