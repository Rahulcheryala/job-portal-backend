# Generated by Django 5.0.6 on 2024-10-09 21:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_remove_jobhirerprofile_job_hirer_ranking_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='years_of_experience',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50.0)]),
        ),
    ]
