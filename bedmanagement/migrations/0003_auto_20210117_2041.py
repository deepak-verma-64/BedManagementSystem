# Generated by Django 2.2.17 on 2021-01-17 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bedmanagement', '0002_auto_20210117_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='bed',
            field=models.ForeignKey(db_column='bed_number', on_delete=django.db.models.deletion.CASCADE, to='bedmanagement.Bed'),
        ),
    ]
