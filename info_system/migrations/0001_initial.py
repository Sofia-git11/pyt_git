

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('model', models.CharField(blank=True, max_length=100, verbose_name='Модель')),
                ('serial_number', models.CharField(blank=True, max_length=50, verbose_name='Серийный номер')),
                ('purchase_date', models.DateField(blank=True, null=True, verbose_name='Дата приобретения')),
                ('warranty_until', models.DateField(blank=True, null=True, verbose_name='Гарантия до')),
                ('status', models.CharField(choices=[('working', 'Исправен'), ('repair', 'На ремонте'), ('out_of_order', 'Неисправен')], default='working', max_length=20, verbose_name='Состояние')),
                ('last_maintenance', models.DateField(blank=True, null=True, verbose_name='Последнее обслуживание')),
            ],
            options={
                'verbose_name': 'Оборудование',
                'verbose_name_plural': 'Оборудование',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('middle_name', models.CharField(blank=True, max_length=100, verbose_name='Отчество')),
                ('birth_date', models.DateField(verbose_name='Дата рождения')),
                ('gender', models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский')], max_length=1, verbose_name='Пол')),
                ('address', models.TextField(blank=True, verbose_name='Адрес')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('insurance_number', models.CharField(blank=True, max_length=20, verbose_name='Страховой номер')),
                ('registration_date', models.DateField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('notes', models.TextField(blank=True, verbose_name='Примечания')),
            ],
            options={
                'verbose_name': 'Пациент',
                'verbose_name_plural': 'Пациенты',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10, unique=True, verbose_name='Номер кабинета')),
                ('floor', models.PositiveIntegerField(verbose_name='Этаж')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Кабинет',
                'verbose_name_plural': 'Кабинеты',
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(choices=[('physiotherapist', 'Физиотерапевт'), ('massage', 'Массажист'), ('rehabilitologist', 'Реабилитолог'), ('nurse', 'Медсестра')], max_length=50, verbose_name='Специализация')),
                ('license_number', models.CharField(blank=True, max_length=50, verbose_name='Номер лицензии')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='info_system.room', verbose_name='Кабинет')),
            ],
            options={
                'verbose_name': 'Врач',
                'verbose_name_plural': 'Врачи',
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateTimeField(verbose_name='Дата и время приёма')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время окончания')),
                ('status', models.CharField(choices=[('scheduled', 'Запланировано'), ('completed', 'Завершено'), ('canceled', 'Отменено'), ('no_show', 'Пациент не явился')], default='scheduled', max_length=20, verbose_name='Статус')),
                ('notes', models.TextField(blank=True, verbose_name='Примечания')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info_system.doctor', verbose_name='Врач')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info_system.patient', verbose_name='Пациент')),
            ],
            options={
                'verbose_name': 'Запись на процедуру',
                'verbose_name_plural': 'Записи на процедуры',
                'ordering': ['appointment_date'],
            },
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.TextField(blank=True, verbose_name='Диагноз')),
                ('recommendations', models.TextField(blank=True, verbose_name='Рекомендации')),
                ('prescription', models.TextField(blank=True, verbose_name='Назначения')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info_system.appointment', verbose_name='Запись на процедуру')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info_system.patient', verbose_name='Пациент')),
            ],
            options={
                'verbose_name': 'Медицинская запись',
                'verbose_name_plural': 'Медицинские записи',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название процедуры')),
                ('procedure_type', models.CharField(choices=[('electro', 'Электротерапия'), ('magnet', 'Магнитотерапия'), ('laser', 'Лазеротерапия'), ('ultrasound', 'Ультразвуковая терапия'), ('massage', 'Массаж'), ('exercise', 'Лечебная физкультура'), ('inhalation', 'Ингаляция')], max_length=50, verbose_name='Тип процедуры')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('duration', models.PositiveIntegerField(verbose_name='Длительность (мин)')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость')),
                ('required_equipment', models.ManyToManyField(blank=True, to='info_system.equipment', verbose_name='Требуемое оборудование')),
            ],
            options={
                'verbose_name': 'Процедура',
                'verbose_name_plural': 'Процедуры',
            },
        ),
        migrations.AddField(
            model_name='appointment',
            name='procedure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info_system.procedure', verbose_name='Процедура'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='info_system.room', verbose_name='Кабинет'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info_system.room', verbose_name='Кабинет'),
        ),
    ]
