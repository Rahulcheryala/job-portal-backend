# Generated by Django 5.1.1 on 2024-09-22 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0008_remove_job_invoice_address_remove_job_invoice_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='employee_type',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
