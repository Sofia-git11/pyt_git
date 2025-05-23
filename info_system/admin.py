from django.contrib import admin
from .models import (
    Patient, Doctor, Procedure, Room,
    Equipment, Appointment, MedicalRecord
)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'birth_date', 'gender', 'phone')
    search_fields = ('last_name', 'first_name', 'phone', 'email')
    list_filter = ('gender', 'registration_date')
    ordering = ('last_name', 'first_name')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'phone', 'room')
    search_fields = ('user__first_name', 'user__last_name', 'phone')
    list_filter = ('specialization',)

@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('name', 'procedure_type', 'duration')
    list_filter = ('procedure_type',)
    search_fields = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'floor')
    search_fields = ('number',)
    list_filter = ('floor',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'status', 'room', 'last_maintenance')
    list_filter = ('status', 'room')
    search_fields = ('name', 'model', 'serial_number')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'procedure', 'doctor', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date', 'doctor')
    search_fields = ('patient__last_name', 'procedure__name', 'doctor__user__last_name')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'appointment', 'created_at')
    search_fields = ('patient__last_name', 'diagnosis', 'recommendations')
    list_filter = ('created_at',)
