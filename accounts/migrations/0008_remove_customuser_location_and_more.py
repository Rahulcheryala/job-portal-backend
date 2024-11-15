# Generated by Django 5.0.6 on 2024-06-22 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_employment_user_remove_project_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='location',
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes/'),
        ),
    ]
