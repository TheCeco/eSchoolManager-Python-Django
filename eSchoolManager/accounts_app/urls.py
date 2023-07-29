from django.urls import path

from .views import SchoolUserLoginView, SchoolUserRegisterView, SchoolUserLogoutView

urlpatterns = [
    path('login/', SchoolUserLoginView.as_view(), name='login'),
    path('register/', SchoolUserRegisterView.as_view(), name='register'),
    path('logout/', SchoolUserLogoutView.as_view(), name='logout'),
]
