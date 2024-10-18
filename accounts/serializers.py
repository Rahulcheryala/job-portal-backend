# from .models import CustomUser, Education, WorkExperience
# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth import authenticate
# from rest_framework import serializers
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.contrib.auth import get_user_model
# from django.core.mail import send_mail
# from django.conf import settings
# from jobportal.settings import DEFAULT_FROM_EMAIL
# from django.core.mail import send_mail
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.template.loader import render_to_string
# from django.contrib.auth.tokens import default_token_generator
# from django.conf import settings


# CustomUser = get_user_model()

# # Serializer for registering job seekers


# class JobSeekerRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'password', 'email', 'username',
#                   'location', 'phone_number', 'technical_skills', 'years_of_experience')
#         extra_kwargs = {'password': {'write_only': True}}
# # Create a new job seeker user

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             first_name=validated_data.get('first_name', ''),
#             last_name=validated_data.get('last_name', ''),
#             username=validated_data['username'],
#             password=validated_data['password'],
#             email=validated_data['email'],
#             location=validated_data.get('location', ''),
#             phone_number=validated_data.get('phone_number', ''),
#             technical_skills=validated_data.get('technical_skills', ''),
#             years_of_experience=validated_data.get('years_of_experience', 0),
#             account_type='job_seeker',
#             is_active=False  # User is inactive until email verification
#         )
#         self.send_verification_email(user)
#         return user
#   # Send verification email to the user

#     def send_verification_email(self, user):
#         request = self.context.get('request')
#         current_site = get_current_site(request)
#         mail_subject = 'Activate your account.'
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         token = default_token_generator.make_token(user)

#         print(f'UID: {uid}')  # Debugging line
#         print(f'Token: {token}')  # Debugging line

#         message = render_to_string('account/activation_email.html', {
#             'user': user,
#             # 'domain': "16.171.14.53:8000",
#             'domain': '127.0.0.1:8000',
#             'uidb64': uid,
#             'token': token,
#         })
#         send_mail(mail_subject, message,
#                   settings.DEFAULT_FROM_EMAIL, [user.email])
# # Serializer for registering job hirers


# class JobHirerRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'password', 'phone_number', 'username',
#                   'working_email', 'hiring_skills', 'how_heard_about_codeunity', 'looking_for')
#         extra_kwargs = {'password': {'write_only': True}}

#      # Create a new job hirer user
#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             first_name=validated_data.get('first_name', ''),
#             last_name=validated_data.get('last_name', ''),
#             username=validated_data['username'],
#             password=validated_data['password'],
#             working_email=validated_data['working_email'],
#             # Use working_email as email
#             email=validated_data['working_email'],
#             phone_number=validated_data.get('phone_number', ''),
#             hiring_skills=validated_data.get('hiring_skills', ''),
#             how_heard_about_codeunity=validated_data.get(
#                 'how_heard_about_codeunity', ''),
#             looking_for=validated_data.get('looking_for', ''),
#             account_type='job_hirer',
#             is_active=False  # User is inactive until email verification
#         )
#         self.send_verification_email(user)
#         return user
#     # Send verification email to the user

#     def send_verification_email(self, user):
#         request = self.context.get('request')
#         current_site = get_current_site(request)
#         mail_subject = 'Activate your account.'
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         token = default_token_generator.make_token(user)

#         print(f'UID: {uid}')  # Debugging line
#         print(f'Token: {token}')  # Debugging line

#         message = render_to_string('account/activation_email.html', {
#             'user': user,
#             # 'domain': "16.171.14.53:8000",
#             'domain': '127.0.0.1:8000',
#             'uidb64': uid,
#             'token': token,
#         })
#         send_mail(mail_subject,
#                   message,
#                   settings.DEFAULT_FROM_EMAIL,
#                   [user.email])

# # Serializer for education details


# class EducationSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(required=False)

#     class Meta:
#         model = Education
#         fields = ['id', 'college_name',
#                   'year_of_graduation', 'degree', 'major', 'gpa']


# class WorkExperienceSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(required=False)

#     class Meta:
#         model = WorkExperience
#         fields = ['id', 'company_name', 'title', 'start_date',
#                   'end_date', 'currently_working', 'description']


# RACE_ETHNICITY_CHOICES = [
#     'Black / African-American',
#     'East Asian (including Chinese, Japanese, Korean, and Mongolian)',
#     'Hispanic or Latino/a/x',
#     'Middle Eastern',
#     'Native American or Alaskan Native',
#     'Pacific Islander',
#     'South Asian (including Bangladeshi, Bhutanese, Indian, Nepali, Pakistani, and Sri Lankan)',
#     'Southeast Asian (including Burmese, Cambodian, Filipino, Hmong, Indonesian, Laotian, Malaysian, Mien, Singaporean, Thai, and Vietnamese)',
#     'White',
#     'Prefer not to say',
#     'Self-describe'
# ]


# class ProfileSerializer(serializers.ModelSerializer):
#     education_details = EducationSerializer(many=True, required=False)
#     work_experience_details = WorkExperienceSerializer(
#         many=True, required=False)
#     open_to_roles = serializers.ListField(
#         child=serializers.CharField(max_length=255), required=False)
#     primary_role = serializers.CharField(max_length=255, required=False)
#     achievements = serializers.CharField(max_length=1000, required=False)
#     pronouns = serializers.CharField(max_length=50, required=False)
#     race_ethnicity = serializers.ListField(
#         child=serializers.ChoiceField(choices=RACE_ETHNICITY_CHOICES),
#         required=False
#     )

#     class Meta:
#         model = CustomUser
#         fields = (
#             'first_name', 'last_name', 'phone_number', 'location', 'technical_skills', 'bio',
#             'country', 'gender', 'website', 'telegram', 'github', 'x',
#             'linkedin', 'instagram', 'spoken_languages', 'available_for_work_from_date',
#             'preferred_annual_pay', 'preferred_hourly_pay', 'resume', 'profile_picture',
#             'company_name', 'designation', 'company_description', 'company_stage', 'product_service',
#             'company_photo', 'working_email', 'years_of_experience', 'email', 'education_details',
#             'work_experience_details', 'open_to_roles', 'primary_role', 'achievements',
#             'pronouns', 'race_ethnicity', 'account_type', 'job_seeker_ranking', 'job_hirer_ranking', 'hiring_skills'
#         )

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         if instance.account_type == 'job_seeker':
#             job_seeker_fields = [
#                 'first_name', 'last_name', 'phone_number', 'email', 'location', 'technical_skills',
#                 'bio', 'country', 'gender', 'website', 'telegram', 'github', 'x',
#                 'linkedin', 'instagram', 'spoken_languages', 'available_for_work_from_date',
#                 'preferred_annual_pay', 'preferred_hourly_pay', 'resume', 'profile_picture',
#                 'years_of_experience', 'education_details', 'work_experience_details',
#                 'open_to_roles', 'primary_role', 'achievements', 'pronouns', 'race_ethnicity', 'account_type'
#             ]
#             # return {field: representation.get(field, None) for field in job_seeker_fields}
#             representation['filled_fields'] = sum(
#                 1 for field in job_seeker_fields if representation[field])
#             representation['total_fields'] = len(job_seeker_fields)
#             representation['job_seeker_ranking'] = instance.calculate_job_seeker_ranking(
#             )
#         elif instance.account_type == 'job_hirer':
#             job_hirer_fields = [
#                 'first_name', 'last_name', 'phone_number', 'company_name', 'designation',
#                 'company_description', 'company_stage', 'product_service', 'company_photo',
#                 'working_email', 'profile_picture', 'gender', 'website', 'telegram',
#                 'github', 'x', 'linkedin', 'account_type', 'hiring_skills'
#             ]
#             # return {field: representation.get(field, None) for field in job_hirer_fields}
#             representation['filled_fields'] = sum(
#                 1 for field in job_hirer_fields if representation[field])
#             representation['total_fields'] = len(job_hirer_fields)
#             representation['job_hirer_ranking'] = instance.calculate_job_hirer_ranking(
#             )
#         return representation

#     def to_internal_value(self, data):   # Handle internal value customization
#         internal_value = super().to_internal_value(data)
#         work_experience_details = internal_value.get(
#             'work_experience_details', [])
#         for work_experience in work_experience_details:
#             if work_experience.get('currently_working'):
#                 work_experience['end_date'] = None
#         return internal_value

#     def update(self, instance, validated_data):
#         # Update the education details
#         education_data = validated_data.pop('education_details', None)
#         if education_data is not None:
#             existing_ids = [item['id']
#                             for item in education_data if 'id' in item]
#             instance.education_details.exclude(id__in=existing_ids).delete()
#             for edu_data in education_data:
#                 if 'id' in edu_data:
#                     edu = Education.objects.get(
#                         id=edu_data['id'], user=instance)
#                     for key, value in edu_data.items():
#                         setattr(edu, key, value)
#                     edu.save()
#                 else:
#                     Education.objects.create(user=instance, **edu_data)

#         # Update the work experience details
#         work_experience_data = validated_data.pop(
#             'work_experience_details', None)
#         if work_experience_data is not None:
#             existing_ids = [item['id']
#                             for item in work_experience_data if 'id' in item]
#             instance.work_experience_details.exclude(
#                 id__in=existing_ids).delete()
#             for work_data in work_experience_data:
#                 if 'id' in work_data:
#                     work = WorkExperience.objects.get(
#                         id=work_data['id'], user=instance)
#                     for key, value in work_data.items():
#                         setattr(work, key, value)
#                     work.save()
#                 else:
#                     WorkExperience.objects.create(user=instance, **work_data)

#         # Update the rest of the fields
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()

#         return instance


# # Serializer for JWT token customization
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username'] = user.username
#         return token

# # Serializer for password reset request


# class PasswordResetRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate_email(self, value):
#         try:
#             user = CustomUser.objects.get(email=value)
#         except CustomUser.DoesNotExist:
#             raise serializers.ValidationError(
#                 "User with this email does not exist.")
#         return value

#     def save(self):
#         request = self.context.get('request')
#         email = self.validated_data['email']
#         user = CustomUser.objects.get(email=email)
#         token = default_token_generator.make_token(user)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         # to redirect the frontend Reset-passwords page
#         frontend_url = f"http://localhost:3000/reset-password/{uid}/{token}/"

#         # Send password reset email
#         send_mail(
#             'Password Reset Request',
#             f'Please click the link below to reset your password: {
#                 frontend_url}',
#             settings.EMAIL_HOST_USER,
#             [email],
#             fail_silently=False,
#         )


# class ResumeUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['resume']


# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = '__all__'


from botocore.exceptions import NoCredentialsError, ClientError
import boto3
from .models import CustomUser, PersonalInfo, JobSeekerProfile, JobHirerProfile, Education, WorkExperience, SocialProfile
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import transaction
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

User = get_user_model()


def send_verification_email(user, request):
    # request = self.context.get('request')  # Get the request object
    current_site = get_current_site(request)  # Get the current site domain
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))  # Encode user ID
    token = default_token_generator.make_token(user)  # Generate the token

    # Debugging lines to check UID and Token in logs
    print(f'UID: {uidb64}')
    print(f'Token: {token}')

    context = {
        'domain': '127.0.0.1:8000',
        'company_name': 'CodeUnity',
        'support': 'codeunity',
        'user': user,
        'uidb64': uidb64,
        'token': token,
    }

    # Render the email body from the template with dynamic data
    message = render_to_string('account/activation_email.html', context)

    # Try sending the email and handle any exceptions
    try:
        send_mail(
            'Activate your account',  # Email subject
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],  # Send to the user's email
            fail_silently=False,  # Raise an error if email fails
            html_message=message  # Send email in HTML format
        )
    except Exception as e:
        # Handle or log email sending errors
        print(f"Error sending email: {e}")


class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = ['phone_number', 'how_heard_about_company']


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = ['location', 'years_of_experience', 'technical_skills']


class JobSeekerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # Nested serializer for personal info
    personal_info = PersonalInfoSerializer(write_only=True)
    # Nested serializer for job seeker profile
    job_seeker_profile = JobSeekerProfileSerializer(
        write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',
                  'password', 'personal_info', 'job_seeker_profile')

    def create(self, validated_data):
        # Extract nested data for personal_info and job_seeker_profile
        personal_info_data = validated_data.pop('personal_info')
        job_seeker_profile_data = validated_data.pop('job_seeker_profile')

        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            account_type='job_seeker',  # Immutable account type
            is_active=False  # Set is_active to False
        )

        # Create related PersonalInfo and JobSeekerProfile entries
        PersonalInfo.objects.create(user=user, **personal_info_data)
        JobSeekerProfile.objects.create(user=user, **job_seeker_profile_data)

        # Send verification email
        send_verification_email(user, self.context.get('request'))

        return user


class JobHirerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobHirerProfile
        fields = ['work_email', 'looking_for']


class JobHirerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # Nested serializer for personal info
    personal_info = PersonalInfoSerializer(write_only=True)
    # Nested serializer for job seeker profile
    job_hirer_profile = JobHirerProfileSerializer(
        write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',
                  'password', 'personal_info', 'job_hirer_profile')

    def create(self, validated_data):
        # Extract nested data for personal_info and job_seeker_profile
        personal_info_data = validated_data.pop('personal_info')
        job_hirer_profile_data = validated_data.pop('job_hirer_profile')

        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            account_type='job_hirer',  # Immutable account type
            is_active=False  # Set is_active to False
        )

        # Create related PersonalInfo and JobSeekerProfile entries
        PersonalInfo.objects.create(user=user, **personal_info_data)
        JobHirerProfile.objects.create(user=user, **job_hirer_profile_data)

        # Send verification email
        send_verification_email(user, self.context.get('request'))

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['account_type'] = user.account_type
        return token

    def validate(self, attrs):
        # Perform the initial validation
        data = super().validate(attrs)

        # Check if the user's email is activated
        if not self.user.is_active:
            # Return a custom response with a specific status code (403 Forbidden)
            return Response({
                'detail': 'Email is not activated.'
            }, status=status.HTTP_403_FORBIDDEN)

        # Add the account_type to the response data
        data['account_type'] = self.user.account_type
        return data


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Include the fields you want to display in the API response
        fields = ('username', 'email', 'first_name', 'last_name',
                  'account_type', 'profile_picture_url')


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('user', None)  # Remove the user field
        return representation


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('user', None)  # Remove the user field
        return representation


class SocialProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialProfile
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('user', None)  # Remove the user field
        return representation


class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('user', None)  # Remove the user field
        return representation


class JobHirerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobHirerProfile
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('user', None)  # Remove the user field
        return representation


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('user', None)  # Remove the user field
        return representation


class ProfileSerializer(serializers.ModelSerializer):
    education_details = EducationSerializer(many=True, required=False)
    work_experience_details = WorkExperienceSerializer(
        many=True, required=False)
    social_profile = SocialProfileSerializer(required=False)
    personal_info = PersonalInfoSerializer(required=False)
    job_seeker_profile = JobSeekerProfileSerializer(required=False)
    job_hirer_profile = JobHirerProfileSerializer(required=False)

    class Meta:
        model = CustomUser
        exclude = [
            'id',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
            'last_login',
            'date_joined',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.account_type == 'job_seeker':
            representation['education_details'] = EducationSerializer(
                instance.job_seeker_profile.education_details.all(), many=True
            ).data
            representation['work_experience_details'] = WorkExperienceSerializer(
                instance.job_seeker_profile.work_experience_details.all(), many=True
            ).data
            representation.pop('job_hirer_profile', None)
        elif instance.account_type == 'job_hirer':
            representation.pop('education_details', None)
            representation.pop('work_experience_details', None)
            representation.pop('job_seeker_profile', None)

        return representation

    @transaction.atomic
    def update(self, instance, validated_data):
        # Update CustomUser fields
        for attr, value in validated_data.items():
            if attr not in ['education_details', 'work_experience_details', 'social_profile', 'personal_info', 'job_seeker_profile', 'job_hirer_profile']:
                setattr(instance, attr, value)
        instance.save()

        # Update or create SocialProfile
        social_profile_data = validated_data.get('social_profile')
        if social_profile_data:
            SocialProfile.objects.update_or_create(
                user=instance, defaults=social_profile_data)

        # Update or create PersonalInfo
        personal_info_data = validated_data.get('personal_info')
        if personal_info_data:
            PersonalInfo.objects.update_or_create(
                user=instance, defaults=personal_info_data)

        # Update JobSeekerProfile or JobHirerProfile based on account_type
        if instance.account_type == 'job_seeker':
            job_seeker_data = validated_data.get('job_seeker_profile')
            if job_seeker_data:
                job_seeker_profile, _ = JobSeekerProfile.objects.update_or_create(
                    user=instance, defaults=job_seeker_data)
            else:
                job_seeker_profile, _ = JobSeekerProfile.objects.get_or_create(
                    user=instance)

            # Handle education details
            education_data = validated_data.get('education_details', [])
            self.update_or_create_related(
                job_seeker_profile, 'education_details', Education, education_data)

            # Handle work experience details
            work_experience_data = validated_data.get(
                'work_experience_details', [])
            self.update_or_create_related(
                job_seeker_profile, 'work_experience_details', WorkExperience, work_experience_data)

        elif instance.account_type == 'job_hirer':
            job_hirer_data = validated_data.get('job_hirer_profile')
            if job_hirer_data:
                JobHirerProfile.objects.update_or_create(
                    user=instance, defaults=job_hirer_data)

        return instance

    def update_or_create_related(self, profile, relation_name, model, data_list):
        existing_items = getattr(profile, relation_name).all()
        existing_ids = set(existing_items.values_list('id', flat=True))

        for item_data in data_list:
            item_id = item_data.get('id')
            if item_id:
                # Update existing item
                model.objects.filter(
                    id=item_id, user=profile).update(**item_data)
                existing_ids.remove(item_id)
            else:
                # Create new item
                model.objects.create(user=profile, **item_data)

        # Delete items that weren't updated
        model.objects.filter(id__in=existing_ids, user=profile).delete()


class ResumeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = ['resume']

    def validate_resume(self, value):
        # Optional: Validate that the uploaded file is a PDF
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        return value


# Serializer for password reset request
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                "User with this email does not exist.")
        return value

    def save(self):
        request = self.context.get('request')
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # to redirect the frontend Reset-passwords page
        frontend_url = f"http://{
            settings.BASE_FRONTEND_URL}/reset-password/{uid}/{token}/"

        # Example context data for the email
        context = {
            'user_name': user.username,
            'reset_link': frontend_url,  # The password reset URL
            'company_name': 'CodeUnity',  # Your company name
        }

        # Render the email body using the template
        email_body = render_to_string('password_reset_email.html', context)

        # Send email
        send_mail(
            'Password Reset Request',
            email_body,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
            html_message=email_body  # This makes sure the email is sent as HTML
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Retrieve the uidb64 and token from the context passed by the view
        uidb64 = self.context.get('uidb64')
        token = self.context.get('token')

        try:
            # Decode the user ID from the uidb64
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(CustomUser, pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError("Invalid UID")

        # Check if the token is valid
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError("Invalid or expired token")

        # Everything is valid, store the user in the validated data for use in `save()`
        attrs['user'] = user
        return attrs

    def save(self):
        # Set the new password for the user
        user = self.validated_data['user']
        user.password = make_password(self.validated_data['new_password'])
        user.save()
        return user


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def upload_file_to_s3(self):
        uploaded_file = self.validated_data['file']

        # Initialize S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        try:
            # Directly upload the file to S3 without saving locally
            s3.upload_fileobj(
                uploaded_file.file,  # access the underlying file-like object
                settings.AWS_STORAGE_BUCKET_NAME,
                uploaded_file.name
            )

            # Generate the S3 file URL
            s3_file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{
                settings.AWS_S3_REGION_NAME}.amazonaws.com/{uploaded_file.name}"

            return s3_file_url

        except (NoCredentialsError, ClientError) as e:
            raise serializers.ValidationError({'error': str(e)})
