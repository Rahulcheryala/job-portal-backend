# Generated by Django 5.0.6 on 2024-10-10 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_rename_how_heard_about_codeunity_personalinfo_how_heard_about_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='years_of_experience',
            field=models.CharField(blank=True, choices=[('Less than 1 year', 'Less than 1 year'), ('1 year', '1 year'), ('2 years', '2 years'), ('3 years', '3 years'), ('4 years', '4 years'), ('5 years', '5 years'), ('6 years', '6 years'), ('7 years', '7 years'), ('8 years', '8 years'), ('9 years', '9 years'), ('10+ years', '10+ years')], max_length=50, null=True),
        ),
    ]
