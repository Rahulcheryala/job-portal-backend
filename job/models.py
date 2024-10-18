from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.conf import settings

from accounts.models import JobHirerProfile, JobSeekerProfile

# class Job(models.Model):  # Model to represent a job posting
#     company_name = models.CharField(max_length=255)  # Company name for the job posting
#     # company_twitter = models.CharField(max_length=255, null=True, blank=True) # Company Twitter handle, optional
#     company_email = models.EmailField() # Company email address
#     position = models.CharField(max_length=255) # Job position title
#     tags = models.CharField(max_length=255) # Tags for the job
#     primary_tag = models.CharField(max_length=255) # Primary tag for the job
#     location_restriction = models.CharField(max_length=255) # Location restriction for the job
#     currency_type = models.CharField(max_length=255) # Currency type for the salary
#     annual_salary_min = models.DecimalField(max_digits=10, decimal_places=2) # Minimum annual salary
#     annual_salary_max = models.DecimalField(max_digits=10, decimal_places=2)  # Maximum annual salary
#     job_description = models.TextField()  # Description of the job
#     apply_url = models.URLField(null=True, blank=True)  # URL for job applications, optional
#     apply_email_address = models.EmailField(null=True, blank=True) # Email address for applications, optional
#     benefits = models.TextField() # Benefits offered by the job
#     how_to_apply = models.TextField() # Instructions on how to apply
#     feedback = models.TextField(null=True, blank=True) # Feedback for applicants, optional
#     created_at = models.DateTimeField(auto_now_add=True) # Timestamp when the job was created
#     updated_at = models.DateTimeField(auto_now=True) # Timestamp when the job was last updated
#     employee_type = models.CharField(max_length=255,null=True)  # Employee type (e.g., Full-time, Part-time, Contract)
#     posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs',default=1) # User who posted the job

# # Model to represent a job application
# class JobApplication(models.Model):
#     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications') # Job being applied for
#     applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications') # User applying for the job
#     cover_letter = models.TextField(default='')  # Cover letter for the application
#     resume = models.FileField(upload_to='applications/resumes/', null=True, blank=True) # Resume file, optional
#     applied_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the application was submitted


class Job(models.Model):
    # Job Details
    job_role = models.CharField(max_length=255)
    job_description = models.TextField()
    job_location = models.CharField(max_length=255)
    industry = models.CharField(
        max_length=100, blank=True, null=True)  # Industry field
    employment_type = models.CharField(max_length=20, default='full_time')
    experience_needed = models.CharField(
        max_length=50, default='entry')  # Experience level
    skills_required = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)

    currency_type = models.CharField(max_length=5, default='USD')  # For salary
    annual_salary_min = models.DecimalField(
        max_digits=20, decimal_places=0, blank=True, null=True)  # Optional min salary
    annual_salary_max = models.DecimalField(
        max_digits=20, decimal_places=0, blank=True, null=True)  # Optional max salary

    how_to_apply = models.TextField()  # Details about the application process
    apply_url = models.URLField(blank=True, null=True)
    application_deadline = models.DateTimeField(
        blank=True, null=True)  # Deadline to apply for the job

    # Metadata
    # Auto set the time when created
    created_at = models.DateTimeField(default=timezone.now)
    # Auto-update the time when updated
    updated_at = models.DateTimeField(auto_now=True)

    # Relationships
    # ForeignKey to job_hirer_profile
    posted_by = models.ForeignKey(
        JobHirerProfile, on_delete=models.CASCADE, related_name='jobs')

    # # Access company details via `posted_by` (no need for extra ForeignKeys)
    # @property
    # def company_name(self):
    #     return self.posted_by.company_name

    # @property
    # def company_photo_url(self):
    #     return self.posted_by.company_photo_url

    # @property
    # def company_website(self):
    #     return self.posted_by.company_website


class JobApplication(models.Model):
    # Relationships
    job = models.ForeignKey('Job', on_delete=models.CASCADE,
                            related_name='applications')  # ForeignKey to the Job model
    applicant = models.ForeignKey(
        JobSeekerProfile, on_delete=models.CASCADE, related_name='applications', null=True, blank=True)

    # Application Details
    # Optional cover letter provided by the applicant
    cover_letter = models.TextField(blank=True, null=True)
    # Changed to URLField to store the actual resume URL
    resume_url = models.URLField(blank=True, null=True)

    # Timestamps
    # Auto-filled timestamp for when the application is submitted
    applied_at = models.DateTimeField(default=timezone.now)

    # Status of the application (can be used later for tracking)
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]
    # Status tracking of the application
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='applied')


class Notification(models.Model):  # Model to represent a notification
    # User receiving the notification
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    message = models.TextField()  # Notification message
    # Timestamp when the notification was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Boolean indicating if the notification has been read, default is False
    is_read = models.BooleanField(default=False)


class Payment(models.Model):  # Model to represent a payment
    # User making the payment
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2)  # Amount of the payment
    payment_id = models.CharField(max_length=255)  # ID of the payment
    status = models.CharField(max_length=50)  # Status of the payment
    # Timestamp when the payment was created
    created_at = models.DateTimeField(auto_now_add=True)
