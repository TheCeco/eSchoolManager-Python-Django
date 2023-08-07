from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic as views

from eSchoolManager.accounts_app.forms import SchoolUserEditForm
from eSchoolManager.principal_app.forms import EditPrincipalProfileForm
from eSchoolManager.principal_app.models import PrincipalProfile

UserModel = get_user_model()


@login_required
@permission_required({
    'accounts_app.view_schooluser',
    'principal_app.view_principalprofile'
}, raise_exception=True)
def principal_details_view(request):
    pk = request.user.pk
    profile = get_object_or_404(PrincipalProfile, user_id=pk)

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
        obj = get_object_or_404(UserModel, pk=pk)

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
        p_form = self.form_class2(request.POST or None, instance=self.request.user.principalprofile)

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
