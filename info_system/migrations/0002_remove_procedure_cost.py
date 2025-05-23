

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info_system', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='procedure',
            name='cost',
        ),
    ]
