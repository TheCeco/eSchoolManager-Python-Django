from django.contrib.auth import views as auth_views, get_user_model, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import generic as views
from django.urls import reverse_lazy

from eSchoolManager.accounts_app.forms import SchoolUserRegistrationForm, SchoolUserLoginForm

UserModel = get_user_model()


# Create your views here.
class SchoolUserLoginView(auth_views.LoginView):
    template_name = 'accounts_templates/login.html'
    form_class = SchoolUserLoginForm

    def form_valid(self, form):
        email = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, email=email, password=password)

        if user is not None and user.is_staff:
            return super().form_valid(form)

        return redirect('not_approved')

    def form_invalid(self, form):
        email = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, email=email, password=password)

        if user is None:
            return super().form_invalid(form)

        return redirect('not_approved')


class SchoolUserRegisterView(views.CreateView):
    form_class = SchoolUserRegistrationForm
    template_name = 'accounts_templates/register.html'
    success_url = reverse_lazy('not_approved')


@method_decorator(login_required, name='dispatch')
class SchoolUserLogoutView(auth_views.LogoutView):
    pass
