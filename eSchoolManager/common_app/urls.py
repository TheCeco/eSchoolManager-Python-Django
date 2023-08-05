from django.urls import path

from .views import NotApprovedView, IndexView, AboutView, ContactsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('not_approved/', NotApprovedView.as_view(), name='not_approved'),
    path('about/', AboutView.as_view(), name='about'),
    path('contacts/', ContactsView.as_view(), name='contacts')
]
