from django.contrib.auth import get_user_model
from django.shortcuts import render

from eSchoolManager.accounts_app.models import SchoolUser

UserModel = get_user_model()


# Create your views here.
def index(request):
    return render(request, 'common_templates/index.html')


def not_approved(request):
    return render(request, 'common_templates/not_approved.html')
