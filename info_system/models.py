from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    """Модель пациента"""
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    middle_name = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    birth_date = models.DateField(verbose_name='Дата рождения')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    address = models.TextField(blank=True, verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    insurance_number = models.CharField(max_length=20, blank=True, verbose_name='Страховой номер')
    registration_date = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    
    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}".strip()

class Doctor(models.Model):
    """Модель врача/медперсонала"""
    SPECIALIZATION_CHOICES = [
        ('physiotherapist', 'Физиотерапевт'),
        ('massage', 'Массажист'),
        ('rehabilitologist', 'Реабилитолог'),
        ('nurse', 'Медсестра'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, verbose_name='Специализация')
    license_number = models.CharField(max_length=50, blank=True, verbose_name='Номер лицензии')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Кабинет')
    
    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_specialization_display()})"

class Procedure(models.Model):
    """Модель физиотерапевтической процедуры"""
    PROCEDURE_TYPES = [
        ('electro', 'Электротерапия'),
        ('magnet', 'Магнитотерапия'),
        ('laser', 'Лазеротерапия'),
        ('ultrasound', 'Ультразвуковая терапия'),
        ('massage', 'Массаж'),
        ('exercise', 'Лечебная физкультура'),
        ('inhalation', 'Ингаляция'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Название процедуры')
    procedure_type = models.CharField(max_length=50, choices=PROCEDURE_TYPES, verbose_name='Тип процедуры')
    description = models.TextField(blank=True, verbose_name='Описание')
    duration = models.PositiveIntegerField(verbose_name='Длительность (мин)')
    #cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    required_equipment = models.ManyToManyField('Equipment', blank=True, verbose_name='Требуемое оборудование')
    
    class Meta:
        verbose_name = 'Процедура'
        verbose_name_plural = 'Процедуры'
    
    def __str__(self):
        return self.name

class Room(models.Model):
    """Модель кабинета"""
    number = models.CharField(max_length=10, unique=True, verbose_name='Номер кабинета')
    floor = models.PositiveIntegerField(verbose_name='Этаж')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'
    
    def __str__(self):
        return f"Кабинет {self.number}"

class Equipment(models.Model):
    """Модель оборудования/аппарата"""
    EQUIPMENT_STATUS = [
        ('working', 'Исправен'),
        ('repair', 'На ремонте'),
        ('out_of_order', 'Неисправен'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Название')
    model = models.CharField(max_length=100, blank=True, verbose_name='Модель')
    serial_number = models.CharField(max_length=50, blank=True, verbose_name='Серийный номер')
    purchase_date = models.DateField(blank=True, null=True, verbose_name='Дата приобретения')
    warranty_until = models.DateField(blank=True, null=True, verbose_name='Гарантия до')
    status = models.CharField(max_length=20, choices=EQUIPMENT_STATUS, default='working', verbose_name='Состояние')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Кабинет')
    last_maintenance = models.DateField(blank=True, null=True, verbose_name='Последнее обслуживание')
    
    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'
    
    def __str__(self):
        return f"{self.name} ({self.model or 'без модели'})"

class Appointment(models.Model):
    """Модель записи на процедуру"""
    STATUS_CHOICES = [
        ('scheduled', 'Запланировано'),
        ('completed', 'Завершено'),
        ('canceled', 'Отменено'),
        ('no_show', 'Пациент не явился'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='Пациент')
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, verbose_name='Процедура')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Врач')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Кабинет')
    appointment_date = models.DateTimeField(verbose_name='Дата и время приёма')
    end_date = models.DateTimeField(verbose_name='Дата и время окончания', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', verbose_name='Статус')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    
    class Meta:
        verbose_name = 'Запись на процедуру'
        verbose_name_plural = 'Записи на процедуры'
        ordering = ['appointment_date']
    
    def __str__(self):
        return f"{self.patient} - {self.procedure} ({self.appointment_date})"

class MedicalRecord(models.Model):
    """Модель медицинской записи/истории процедур"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='Пациент')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, verbose_name='Запись на процедуру')
    diagnosis = models.TextField(blank=True, verbose_name='Диагноз')
    recommendations = models.TextField(blank=True, verbose_name='Рекомендации')
    prescription = models.TextField(blank=True, verbose_name='Назначения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')
    
    class Meta:
        verbose_name = 'Медицинская запись'
        verbose_name_plural = 'Медицинские записи'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Запись {self.patient} от {self.created_at.date()}"