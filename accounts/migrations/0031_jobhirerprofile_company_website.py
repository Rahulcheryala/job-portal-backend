# Generated by Django 5.0.6 on 2024-10-17 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_jobhirerprofile_company_photo_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobhirerprofile',
            name='company_website',
            field=models.URLField(blank=True, null=True),
        ),
    ]