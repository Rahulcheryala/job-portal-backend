# from django.db import models
# from django.contrib.auth.models import AbstractUser


# class CustomUser(AbstractUser):
#     # Common fields
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     location = models.CharField(max_length=255, blank=True, null=True)
#     technical_skills = models.TextField(blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     account_type = models.CharField(max_length=50, choices=[(
#         'job_seeker', 'Job Seeker'), ('job_hirer', 'Job Hirer')])
#     country = models.CharField(max_length=100, blank=True, null=True)
#     gender = models.CharField(max_length=50, blank=True, null=True)
#     website = models.URLField(blank=True, null=True)
#     telegram = models.URLField(blank=True, null=True)
#     github = models.URLField(blank=True, null=True)
#     x = models.URLField(blank=True, null=True)
#     linkedin = models.URLField(blank=True, null=True)
#     instagram = models.URLField(blank=True, null=True)
#     spoken_languages = models.CharField(max_length=255, blank=True, null=True)
#     available_for_work_from_date = models.DateField(blank=True, null=True)
#     preferred_annual_pay = models.DecimalField(
#         max_digits=10, decimal_places=2, blank=True, null=True)
#     preferred_hourly_pay = models.DecimalField(
#         max_digits=10, decimal_places=2, blank=True, null=True)
#     resume = models.FileField(upload_to='resumes/', blank=True, null=True)
#     profile_picture = models.ImageField(
#         upload_to='profile_pictures/', blank=True, null=True)
#     profile_picture_url = models.URLField(
#         max_length=200, blank=True, null=True)
#     hiring_skills = models.TextField(blank=True, null=True)
#     technical_skills = models.TextField(blank=True, null=True)
#     how_heard_about_codeunity = models.CharField(
#         max_length=255, blank=True, null=True)
#     looking_for = models.CharField(max_length=255, blank=True, null=True)

#     # Job Hirer specific fields
#     company_name = models.CharField(max_length=255, blank=True, null=True)
#     designation = models.CharField(max_length=255, blank=True, null=True)
#     company_description = models.TextField(blank=True, null=True)
#     company_stage = models.CharField(max_length=100, blank=True, null=True)
#     product_service = models.CharField(max_length=255, blank=True, null=True)
#     company_photo = models.ImageField(
#         upload_to='company_photos/', blank=True, null=True)
#     working_email = models.EmailField(blank=True, null=True)

#     # Job Seeker specific fields
#     years_of_experience = models.DecimalField(
#         max_digits=5, decimal_places=2, blank=True, null=True)
#     open_to_roles = models.CharField(max_length=255, blank=True, null=True)
#     primary_role = models.CharField(max_length=255, blank=True, null=True)
#     achievements = models.TextField(blank=True, null=True)
#     pronouns = models.CharField(max_length=50, blank=True, null=True)
#     # This can be a JSON or Text field if multiple values
#     race_ethnicity = models.CharField(max_length=255, blank=True, null=True)

#     job_seeker_ranking = models.DecimalField(
#         max_digits=5, decimal_places=2, blank=True, null=True)
#     job_hirer_ranking = models.DecimalField(
#         max_digits=5, decimal_places=2, blank=True, null=True)

#     def save(self, *args, **kwargs):
#         # Calculate and set ranking before saving
#         if self.account_type == 'job_seeker':
#             self.job_seeker_ranking = self.calculate_job_seeker_ranking()
#         elif self.account_type == 'job_hirer':
#             self.job_hirer_ranking = self.calculate_job_hirer_ranking()
#         super(CustomUser, self).save(*args, **kwargs)

#     def calculate_job_seeker_ranking(self):
#         job_seeker_fields_to_check = [
#             self.first_name, self.last_name, self.phone_number, self.email, self.location,
#             self.technical_skills, self.bio, self.country, self.gender, self.website,
#             self.telegram, self.github, self.x, self.linkedin, self.instagram,
#             self.spoken_languages, self.available_for_work_from_date, self.preferred_annual_pay,
#             self.preferred_hourly_pay, self.resume, self.profile_picture, self.years_of_experience
#         ]
#         filled_fields = sum(1 for field in job_seeker_fields_to_check if field)
#         total_fields = len(job_seeker_fields_to_check)
#         return round((filled_fields / total_fields) * 100, 2) if total_fields > 0 else 0

#     def calculate_job_hirer_ranking(self):
#         job_hirer_fields_to_check = [
#             self.first_name, self.last_name, self.phone_number, self.company_name,
#             self.designation, self.company_description, self.company_stage, self.product_service,
#             self.company_photo, self.working_email, self.profile_picture, self.gender,
#             self.website, self.telegram, self.github, self.x, self.linkedin, self.hiring_skills
#         ]
#         filled_fields = sum(1 for field in job_hirer_fields_to_check if field)
#         total_fields = len(job_hirer_fields_to_check)
#         return round((filled_fields / total_fields) * 100, 2) if total_fields > 0 else 0

#     def __str__(self):
#         return f"{self.username} ({self.account_type})"


# class Education(models.Model):
#     user = models.ForeignKey(
#         CustomUser, related_name='education_details', on_delete=models.CASCADE)
#     college_name = models.CharField(max_length=255)
#     year_of_graduation = models.IntegerField()
#     degree = models.CharField(max_length=255)
#     major = models.CharField(max_length=255)
#     gpa = models.DecimalField(max_digits=4, decimal_places=2)

#     # def __str__(self):
#     #     return f"{self.college_name} ({self.degree})"


# class WorkExperience(models.Model):
#     user = models.ForeignKey(
#         CustomUser, related_name='work_experience_details', on_delete=models.CASCADE)
#     company_name = models.CharField(max_length=255)
#     title = models.CharField(max_length=255)
#     start_date = models.DateField()
#     end_date = models.DateField(blank=True, null=True)
#     currently_working = models.BooleanField(default=False)
#     description = models.TextField(max_length=1000)

#     # def __str__(self):
#     #     return f"{self.title} at {self.company_name}"


from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CustomUser(AbstractUser):
    account_type = models.CharField(max_length=50, choices=[
        ('job_seeker', 'Job Seeker'),
        ('job_hirer', 'Job Hirer')
    ])
    email = models.EmailField(unique=True)
    profile_picture_url = models.URLField(
        max_length=200, blank=True, null=True)
    # Additional fields from AbstractUser: username, first_name, last_name, password, is_active, is_staff, is_superuser, last_login, date_joined, groups, user_permissions

    class Meta:
        # This allows you to exclude fields from the model
        managed = True  # Set to False if you want Django not to manage the database schema for this model
        # Exclude 'groups' and 'user_permissions' fields from the model
        default_permissions = ()
        permissions = ()


class PersonalInfo(models.Model):
    RACE_ETHNICITY_CHOICES = [
        # (key, value) value is stored in the database, key is displayed in the form
        ('black_african', 'Black / African-American'),
        ('east_asian', 'East Asian (including Chinese, Japanese, Korean, and Mongolian)'),
        ('hispanic_latino', 'Hispanic or Latino/a/x'),
        ('middle_eastern', 'Middle Eastern'),
        ('native_american', 'Native American or Alaskan Native'),
        ('pacific_islander', 'Pacific Islander'),
        ('south_asian', 'South Asian (including Bangladeshi, Bhutanese, Indian, Nepali, Pakistani, and Sri Lankan)'),
        ('southeast_asian', 'Southeast Asian (including Burmese, Cambodian, Filipino, Hmong, Indonesian, Laotian, Malaysian, Mien, Singaporean, Thai, and Vietnamese)'),
        ('white', 'White'),
        ('prefer_not_say', 'Prefer not to say'),
        # ('self_describe', 'Self-describe')
    ]

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='personal_info')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True
    )
    gender = models.CharField(max_length=50, blank=True, null=True)
    gender_self_describe = models.CharField(
        max_length=255, blank=True, null=True
    )
    pronouns = models.CharField(max_length=50, blank=True, null=True)
    pronouns_self_describe = models.CharField(
        max_length=255, blank=True, null=True
    )
    race_ethnicity = models.CharField(
        max_length=50, choices=RACE_ETHNICITY_CHOICES, blank=True, null=True
    )
    how_heard_about_company = models.CharField(
        max_length=255, blank=True, null=True
    )


class JobSeekerProfile(models.Model):
    EXPERIENCE_CHOICES = [
        ('Less than 1 year', 'Less than 1 year'),
        ('1 year', '1 year'),
        ('2 years', '2 years'),
        ('3 years', '3 years'),
        ('4 years', '4 years'),
        ('5 years', '5 years'),
        ('6 years', '6 years'),
        ('7 years', '7 years'),
        ('8 years', '8 years'),
        ('9 years', '9 years'),
        ('10+ years', '10+ years')
    ]
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='job_seeker_profile')
    years_of_experience = models.CharField(
        max_length=50, choices=EXPERIENCE_CHOICES, blank=True, null=True)
    technical_skills = models.TextField(blank=True, null=True)
    # open_to_roles = models.CharField(max_length=255, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    resume_url = models.URLField(max_length=200, blank=True, null=True)
    # primary_role = models.CharField(max_length=255, blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    # available_for_work_from_date = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    # job_seeker_ranking = models.DecimalField(
    #     max_digits=5, decimal_places=2, blank=True, null=True)


class JobHirerProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='job_hirer_profile')
    designation = models.CharField(max_length=255, blank=True, null=True)
    work_email = models.EmailField(blank=True, null=True)
    company_photo = models.ImageField(
        upload_to='company_photos/', blank=True, null=True)
    company_photo_url = models.URLField(max_length=200, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    company_stage = models.CharField(max_length=100, blank=True, null=True)
    company_website = models.URLField(max_length=200, blank=True, null=True)
    product_service = models.CharField(max_length=255, blank=True, null=True)
    looking_for = models.CharField(max_length=50, choices=[
        ('freelance', 'Freelance Contractor'),
        ('full_time', 'Full Time Employee')
    ])
    # job_hirer_ranking = models.DecimalField(
    #     max_digits=5, decimal_places=2, blank=True, null=True)


class SocialProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='social_profile')
    website = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)


class Education(models.Model):
    user = models.ForeignKey(
        JobSeekerProfile, related_name='education_details', on_delete=models.CASCADE)
    college_name = models.CharField(max_length=255)
    year_of_graduation = models.IntegerField()
    degree = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.college_name} ({self.degree})"


class WorkExperience(models.Model):
    user = models.ForeignKey(
        JobSeekerProfile, related_name='work_experience_details', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    currently_working = models.BooleanField(default=False)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.title} at {self.company_name}"
