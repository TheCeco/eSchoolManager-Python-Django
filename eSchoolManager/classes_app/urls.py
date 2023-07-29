from django.urls import path

from .views import ClassesList, ClassDetailsView

urlpatterns = [
    path('list/', ClassesList.as_view(), name='classes_list'),
    path('details/<int:pk>', ClassDetailsView.as_view(), name='classes_details')
]
