# Generated by Django 5.0.6 on 2024-10-09 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_alter_customuser_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personalinfo',
            old_name='how_heard_about_codeunity',
            new_name='how_heard_about_company',
        ),
    ]
