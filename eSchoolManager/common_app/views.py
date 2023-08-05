from django.views import generic as views
from django.contrib.auth import get_user_model
from django.shortcuts import render

from eSchoolManager.accounts_app.models import SchoolUser
from eSchoolManager.common_app.models import SubjectsModel
from eSchoolManager.teachers_app.models import TeacherProfile

UserModel = get_user_model()


# Create your views here.
class IndexView(views.TemplateView):
    template_name = 'common_templates/index.html'


class NotApprovedView(views.TemplateView):
    template_name = 'common_templates/not_approved.html'


class AboutView(views.TemplateView):
    template_name = 'common_templates/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subjects = SubjectsModel.objects.all()
        teachers = TeacherProfile.objects.all()

        context = {
            'subjects': subjects,
            'teachers': teachers
        }

        return context


class ContactsView(views.TemplateView):
    template_name = 'common_templates/contacts.html'
