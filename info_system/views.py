from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Patient, Doctor, Procedure, Room, Equipment, Appointment, MedicalRecord
from .forms import PatientForm, DoctorForm, ProcedureForm, RoomForm, EquipmentForm, AppointmentForm, MedicalRecordForm

# Пациенты
'''Стандартные функции вывода списка'''

class PatientListView(ListView):
    model = Patient
    template_name = 'physiotherapy/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 20

class PatientDetailView(DetailView):
    model = Patient
    template_name = 'physiotherapy/patient_detail.html'

class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'physiotherapy/patient_form.html'
    success_url = reverse_lazy('patient_list')

class PatientUpdateView(UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'physiotherapy/patient_form.html'
    success_url = reverse_lazy('patient_list')

class PatientDeleteView(DeleteView):
    model = Patient
    template_name = 'physiotherapy/patient_confirm_delete.html'
    success_url = reverse_lazy('patient_list')

# Врачи
class DoctorListView(ListView):
    model = Doctor
    template_name = 'physiotherapy/doctor_list.html'
    context_object_name = 'doctors'

class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'physiotherapy/doctor_detail.html'

# Процедуры
class ProcedureListView(ListView):
    model = Procedure
    template_name = 'physiotherapy/procedure_list.html'
    context_object_name = 'procedures'

# Записи на прием
class AppointmentListView(ListView):
    model = Appointment
    template_name = 'physiotherapy/appointment_list.html'
    context_object_name = 'appointments'
    ordering = ['appointment_date']


'''============КОНЕЦ================='''


def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'physiotherapy/appointment_form.html', {'form': form})

def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'physiotherapy/appointment_form.html', {'form': form})

def dashboard(request):
    context = {
      
        'patient_count': Patient.objects.count(),
        'appointment_count': Appointment.objects.count(),
    }
    return render(request, 'physiotherapy/dashboard.html', context)

def personal_account(request):
    # Получаем последние записи для отображения
    recent_data = {
        'patients': Patient.objects.order_by('-registration_date')[:5],
        'appointments': Appointment.objects.order_by('-appointment_date')[:5],
        'procedures': Procedure.objects.order_by('-id')[:5],
    }
    
    context = {
        'recent_data': recent_data,
    }
    
    return render(request, 'physiotherapy/personal_account.html', context)