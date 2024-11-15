# Generated by Django 5.0.6 on 2024-10-13 11:39

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_alter_jobseekerprofile_years_of_experience'),
        ('job', '0010_job_currency_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='location_restriction',
            new_name='job_location',
        ),
        migrations.RenameField(
            model_name='job',
            old_name='position',
            new_name='job_role',
        ),
        migrations.RemoveField(
            model_name='job',
            name='annual_salary_max',
        ),
        migrations.RemoveField(
            model_name='job',
            name='annual_salary_min',
        ),
        migrations.RemoveField(
            model_name='job',
            name='apply_email_address',
        ),
        migrations.RemoveField(
            model_name='job',
            name='company_email',
        ),
        migrations.RemoveField(
            model_name='job',
            name='company_twitter',
        ),
        migrations.RemoveField(
            model_name='job',
            name='employee_type',
        ),
        migrations.RemoveField(
            model_name='job',
            name='feedback',
        ),
        migrations.RemoveField(
            model_name='job',
            name='primary_tag',
        ),
        migrations.RemoveField(
            model_name='job',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='jobapplication',
            name='applicant',
        ),
        migrations.AddField(
            model_name='job',
            name='application_deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='company_logo',
            field=models.ImageField(blank=True, null=True, upload_to='company_logos/'),
        ),
        migrations.AddField(
            model_name='job',
            name='company_logo_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='company_website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='employment_type',
            field=models.CharField(default='full_time', max_length=20),
        ),
        migrations.AddField(
            model_name='job',
            name='experience_needed',
            field=models.CharField(default='entry', max_length=50),
        ),
        migrations.AddField(
            model_name='job',
            name='industry',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='job',
            name='salary_max',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='salary_min',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='skills_required',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='applicant_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='accounts.jobseekerprofile'),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='status',
            field=models.CharField(choices=[('not_applied', 'Not Applied'), ('applied', 'Applied'), ('under_review', 'Under Review'), ('rejected', 'Rejected'), ('accepted', 'Accepted')], default='applied', max_length=20),
        ),
        migrations.AlterField(
            model_name='job',
            name='benefits',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='job',
            name='currency_type',
            field=models.CharField(default='USD', max_length=5),
        ),
        migrations.AlterField(
            model_name='job',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='accounts.jobhirerprofile'),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='applied_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='cover_letter',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='resume',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resumes', to='accounts.jobseekerprofile'),
        ),
    ]
