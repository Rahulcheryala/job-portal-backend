# Generated by Django 5.0.6 on 2024-07-04 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_remove_customuser_hiring_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='hiring_skills',
            field=models.TextField(blank=True, null=True),
        ),
    ]
