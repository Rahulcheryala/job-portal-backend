# Generated by Django 5.0.6 on 2024-10-17 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_rename_working_email_jobhirerprofile_work_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalinfo',
            name='gender_self_describe',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='personalinfo',
            name='pronouns_self_describe',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
