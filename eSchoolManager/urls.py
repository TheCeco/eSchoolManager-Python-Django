"""
URL configuration for eSchoolManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('eSchoolManager.common_app.urls')),
    path('profile/', include('eSchoolManager.accounts_app.urls')),
    path('students/', include('eSchoolManager.students_app.urls')),
    path('teachers/', include('eSchoolManager.teachers_app.urls')),
    path('principal/', include('eSchoolManager.principal_app.urls')),
    path('classes/', include('eSchoolManager.classes_app.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
