# Generated by Django 5.0.6 on 2024-10-08 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0009_job_employee_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='currency_type',
            field=models.CharField(default=2, max_length=255),
            preserve_default=False,
        ),
    ]