# from .models import Job, JobApplication  # Import the Job and JobApplication models
# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# # Serializer for job details, used within other serializers
# class JobDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Job
#         fields = [
#             'company_name',
#             'location_restriction',
#             'tags',
#             'annual_salary_max',
#             'position'
#         ]

# class JobApplicationSerializer(serializers.ModelSerializer):
#     applicant_name = serializers.SerializerMethodField()
#     applicant_email = serializers.SerializerMethodField()
#     applicant_phone = serializers.SerializerMethodField()
#     applicant_profile_picture = serializers.SerializerMethodField()
#     job_details = JobDetailSerializer(source='job', read_only=True)
#     applicant_resume = serializers.SerializerMethodField()  # New field for resume

#     class Meta:
#         model = JobApplication
#         fields = [
#             'job', 'applicant_name', 'applicant_email', 'applicant_phone',
#             'applicant_profile_picture', 'applied_at', 'job_details',
#             'applicant_resume'  # Include the new field in the fields list
#         ]

#     def get_applicant_name(self, obj):
#         return obj.applicant.get_full_name()

#     def get_applicant_email(self, obj):
#         return obj.applicant.email

#     def get_applicant_phone(self, obj):
#         return getattr(obj.applicant, 'phone_number', None)  # Fallback if phone_number is None

#     def get_applicant_profile_picture(self, obj):
#         request = self.context.get('request', None)
#         if request and obj.applicant.profile_picture:
#             return request.build_absolute_uri(obj.applicant.profile_picture.url)
#         return None

#     def get_applicant_resume(self, obj):
#         request = self.context.get('request', None)
#         if request and obj.resume:
#             return request.build_absolute_uri(obj.resume.url)
#         return None

#     def create(self, validated_data):
#         job = validated_data.get('job')
#         applicant = self.context['request'].user
#         resume = getattr(applicant, 'resume', None)  # Fallback if resume is None

#         job_application = JobApplication.objects.create(
#             job=job,
#             applicant=applicant,
#             resume=resume
#         )
#         return job_application

# # Serializer for jobs
# class JobSerializer(serializers.ModelSerializer):
#     applications = serializers.SerializerMethodField()  # Field to include job applications in the serialized output

#     class Meta:
#         model = Job
#         fields = '__all__'
#         read_only_fields = ('posted_by',)

#     # Method to get applications for a job
#     def get_applications(self, obj):
#         user = self.context['request'].user
#         if user.is_authenticated and user.account_type == 'job_hirer':
#             applications = JobApplication.objects.filter(job=obj)
#             return JobApplicationSerializer(applications, many=True).data
#         return None

#     # Validation method to ensure only job hirers can post jobs
#     def validate(self, attrs):
#         user = self.context['request'].user
#         if user.account_type != 'job_hirer':
#             raise serializers.ValidationError("Only job hirers can post jobs.")
#         return attrs


from rest_framework import serializers
from accounts.models import JobHirerProfile, JobSeekerProfile
from job.models import Job, JobApplication


class JobHirerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobHirerProfile
        fields = ['company_name', 'company_website', 'company_photo_url']


class JobDetailSerializer(serializers.ModelSerializer):
    posted_by = JobHirerProfileSerializer(read_only=True)

    class Meta:
        model = Job
        fields = '__all__'  # Include all fields from the Job model


class JobSerializer(serializers.ModelSerializer):
    # Nesting the profile serializer
    posted_by = JobHirerProfileSerializer(read_only=True)

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('posted_by', 'created_at', 'updated_at')

    # Validation method to ensure only job hirers can post jobs
    def validate(self, attrs):
        user = self.context['request'].user
        if user.account_type != 'job_hirer':
            raise serializers.ValidationError(
                "Only job hirers can post or update jobs.")
        return attrs

    def update(self, instance, validated_data):
        """
        This method allows updating specific fields of the Job model.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    # Nested serializer to get CustomUser details
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = JobSeekerProfile
        fields = ['first_name', 'last_name', 'email']


class JobApplicationSerializer(serializers.ModelSerializer):
    # To display job details in the response
    applicant = JobSeekerProfileSerializer(read_only=True)
    job = JobSerializer(read_only=True)

    class Meta:
        model = JobApplication
        # Added additional fields for other views
        fields = ['applicant', 'cover_letter',
                  'status', 'applied_at', 'resume_url', 'job']

    def validate(self, data):
        user = self.context['request'].user
        job = self.context['job']  # job passed from the view

        # Check if the user has already applied for this job
        if JobApplication.objects.filter(applicant=user.job_seeker_profile, job=job).exists():
            raise serializers.ValidationError(
                "You have already applied for this job.")

        return data

    def create(self, validated_data):
        # Get context from view (job and user information)
        job = self.context['job']
        applicant = self.context['request'].user.job_seeker_profile

        # Create the job application
        job_application = JobApplication.objects.create(
            applicant=applicant,
            job=job,
            resume_url=applicant.resume_url,
            cover_letter=validated_data.get('cover_letter', ''),
            status='applied'
        )

        return job_application
