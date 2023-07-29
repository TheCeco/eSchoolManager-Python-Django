from django.urls import path

from .views import not_approved, index

urlpatterns = [
    path('', index, name='index'),
    path('not_approved/', not_approved, name='not_approved')
]
