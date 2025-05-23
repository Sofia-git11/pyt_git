"""
URL configuration for physiotherapy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from info_system import views
from info_system.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('account/', views.personal_account, name='personal_account'),
    
    # Пациенты
    path('patients/', PatientListView.as_view(), name='patient_list'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('patients/add/', PatientCreateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/edit/', PatientUpdateView.as_view(), name='patient_update'),
    path('patients/<int:pk>/delete/', PatientDeleteView.as_view(), name='patient_delete'),
    
    # Врачи
    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor_detail'),
    
    # Процедуры
    path('procedures/', ProcedureListView.as_view(), name='procedure_list'),
    
    # Записи на прием
    path('appointments/', AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/add/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/edit/', views.appointment_update, name='appointment_update'),
]
