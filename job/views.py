from django.db.models import Q
from rest_framework import generics, status
from rest_framework import serializers
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import CustomUser, JobHirerProfile, JobSeekerProfile
from .models import Job, JobApplication, Notification, Payment
from .serializers import JobApplicationSerializer, JobDetailSerializer, JobSerializer
from .pagination import CustomPagination
from job import pagination

# Custom permission to allow only job hirers who are the owners of the job to edit/delete it


# class IsJobHirerAndOwner(permissions.BasePermission):
#     """
#     Custom permission to only allow job hirers who are the owners of the job to edit/delete it.
#     """

#     def has_object_permission(self, request, view, obj):
#         return request.user.account_type == 'job_hirer' and obj.posted_by == request.user


# API view to initiate a payment
# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def initiate_payment(request):
#     user = request.user
#     amount = request.data.get('amount')

#     # Send a POST request to the Node.js server to create a payment order
#     response = requests.post(
#         'http://16.171.14.53/api/payment/orders',  # Node.js server URL
#         json={'userId': user.id, 'amount': amount}
#     )

#     if response.status_code == 200:
#         payment_data = response.json()
#         Payment.objects.create(
#             user=user,
#             amount=amount,
#             # Adjust based on your Node.js response structure
#             payment_id=payment_data['data']['id'],
#             status='initiated'
#         )
#         return Response(payment_data)
#     else:
#         return Response({'error': 'Payment initiation failed'}, status=400)

# # API view to handle payment webhook


# @api_view(['POST'])
# def payment_webhook(request):
#     data = request.data
#     user_id = data.get('userId')
#     payment_id = data.get('paymentId')
#     amount = data.get('amount')
#     status = data.get('status')

#     try:
#         payment = Payment.objects.get(payment_id=payment_id)
#         payment.status = status
#         payment.save()

#         return Response({'status': 'Payment updated successfully'})
#     except Payment.DoesNotExist:
#         return Response({'error': 'Payment not found'}, status=404)


# View to list all jobs with filtering and sorting options
class JobListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = JobSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        page = self.request.query_params.get('page')
        print("Requested page:", page)
        queryset = Job.objects.all()

        # Filtering by job location
        job_location = self.request.query_params.get('job_location', None)
        if job_location:
            queryset = queryset.filter(job_location__icontains=job_location)

        # Filtering by salary range
        annual_salary_min = self.request.query_params.get(
            'annual_salary_min', None)
        annual_salary_max = self.request.query_params.get(
            'annual_salary_max', None)
        if annual_salary_min and annual_salary_max:
            queryset = queryset.filter(
                Q(annual_salary_min__gte=annual_salary_min) &
                Q(annual_salary_max__lte=annual_salary_max)
            )
        elif annual_salary_min:
            queryset = queryset.filter(
                annual_salary_min__gte=annual_salary_min)
        elif annual_salary_max:
            queryset = queryset.filter(
                annual_salary_max__lte=annual_salary_max)

        # Filtering by employment type
        employment_type = self.request.query_params.get(
            'employment_type', None)
        if employment_type:
            queryset = queryset.filter(
                employment_type__icontains=employment_type)

        # Filtering by industry
        industry = self.request.query_params.get('industry', None)
        if industry:
            queryset = queryset.filter(industry__icontains=industry)

        # Filtering by skills (skills_required)
        skills_required = self.request.query_params.get(
            'skills_required', None)
        if skills_required:
            skills_list = [skill.strip().lower()
                           for skill in skills_required.split(',')]
            query = Q()
            for skill in skills_list:
                # This will match partial strings within the CSV
                query |= Q(skills_required__iregex=rf'\y{skill}\y')
            queryset = queryset.filter(query).distinct()

         # Sorting
        sort_by = self.request.query_params.get('sort_by', 'latest')
        sort_mapping = {
            'latest': '-created_at',
            'highest_salary': '-salary_max',
            'lowest_salary': 'salary_min',
        }
        queryset = queryset.order_by(sort_mapping.get(sort_by, '-created_at'))
        return queryset

    # Adding request context to the serializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# View to create a job
class JobCreateView(generics.CreateAPIView):
    queryset = Job.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer

    # Override the perform_create method to check job posting limit and payment status
    def perform_create(self, serializer):
        user = self.request.user
        # Retrieve the JobHirerProfile associated with the logged-in user
        try:
            job_hirer_profile = user.job_hirer_profile  # Assuming OneToOne relationship
        except JobHirerProfile.DoesNotExist:
            raise serializers.ValidationError(
                "User does not have a JobHirerProfile associated.")

        # job_count = Job.objects.filter(posted_by=user).count()

        # Check if the user has posted more than one job without completing a payment
        # if job_count >= 1:
        #     if not Payment.objects.filter(user=user, status='completed').exists():
        #         raise PermissionDenied(
        #             'Payment required for additional job postings.')

        serializer.save(posted_by=job_hirer_profile)


# View to get all jobs posted by a hirer
class PostedJobsListView(generics.ListAPIView):
    # Ensure that the user is authenticated
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        # Get the logged-in user (assumed to be a job hirer)
        user = self.request.user

        # Ensure the user is a job hirer
        try:
            job_hirer_profile = JobHirerProfile.objects.get(user=user)
        except JobHirerProfile.DoesNotExist:
            return Job.objects.none()  # Return no jobs if the user is not a job hirer

        # Start with jobs posted by the authenticated hirer
        queryset = Job.objects.filter(posted_by=job_hirer_profile)

        # Filtering by job location
        job_location = self.request.query_params.get('job_location', None)
        if job_location:
            queryset = queryset.filter(job_location__icontains=job_location)

        # Filtering by salary range
        annual_salary_min = self.request.query_params.get(
            'annual_salary_min', None)
        annual_salary_max = self.request.query_params.get(
            'annual_salary_max', None)
        if annual_salary_min and annual_salary_max:
            queryset = queryset.filter(
                Q(annual_salary_min__gte=annual_salary_min) &
                Q(annual_salary_max__lte=annual_salary_max)
            )
        elif annual_salary_min:
            queryset = queryset.filter(
                annual_salary_min__gte=annual_salary_min)
        elif annual_salary_max:
            queryset = queryset.filter(
                annual_salary_max__lte=annual_salary_max)

        # Filtering by employment type
        employment_type = self.request.query_params.get(
            'employment_type', None)
        if employment_type:
            queryset = queryset.filter(
                employment_type__icontains=employment_type)

        # Filtering by industry
        industry = self.request.query_params.get('industry', None)
        if industry:
            queryset = queryset.filter(industry__icontains=industry)

        # Filtering by skills (skills_required)
        skills_required = self.request.query_params.get(
            'skills_required', None)
        if skills_required:
            skills_list = [skill.strip().lower()
                           for skill in skills_required.split(',')]
            query = Q()
            for skill in skills_list:
                # This will match partial strings within the CSV
                query |= Q(skills_required__iregex=rf'\y{skill}\y')
            queryset = queryset.filter(query).distinct()

         # Sorting
        sort_by = self.request.query_params.get('sort_by', 'latest')
        sort_mapping = {
            'latest': '-created_at',
            'highest_salary': '-salary_max',
            'lowest_salary': 'salary_min',
        }
        queryset = queryset.order_by(sort_mapping.get(sort_by, '-created_at'))
        return queryset

    # Add request to serializer context
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class JobDetailsView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    # Allows access to any user, whether authenticated or not
    permission_classes = [AllowAny]
    lookup_field = 'pk'  # Look up by primary key

    def get(self, request, *args, **kwargs):
        job = self.get_object()  # Retrieves the job based on the primary key in the URL
        serializer = self.get_serializer(job)
        return Response(serializer.data)


# View to update a job
class JobUpdateView(generics.UpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'  # To find the job by its ID (primary key)

    # Override the update method to check for permissions
    def update(self, request, *args, **kwargs):
        job = self.get_object()  # Get the job instance by ID
        user = request.user

        # Check if the logged-in user is the job hirer who posted the job
        if job.posted_by != user.job_hirer_profile:
            raise PermissionDenied(
                "You do not have permission to update this job.")

        # If everything is valid, perform the update
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(
            job, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        # Save the updated job
        serializer.save()


# View to delete a job
class JobDeleteView(generics.DestroyAPIView):
    queryset = Job.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override get_queryset to ensure that only jobs owned by the user can be deleted.
        """
        user = self.request.user
        if user.account_type != 'job_hirer':
            raise PermissionDenied("Only job hirers can delete jobs.")

        # Only return jobs posted by the logged-in user
        return Job.objects.filter(posted_by=user.job_hirer_profile)

    def delete(self, request, *args, **kwargs):
        """
        Perform the deletion only if the user is the owner of the job.
        """
        job = self.get_object()
        if job.posted_by != request.user.job_hirer_profile:
            raise PermissionDenied("You are not allowed to delete this job.")

        return super().delete(request, *args, **kwargs)


# View to apply for a job
class JobApplyView(generics.CreateAPIView):
    serializer_class = JobApplicationSerializer
    # Ensure only authenticated users can apply
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        # Get the context and include the job object
        context = super().get_serializer_context()

        # Get the job from the URL (job_id passed via URL)
        job_id = self.kwargs['pk']
        try:
            job = Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            raise ValidationError(
                "The job you're trying to apply for does not exist.")

        context['job'] = job  # Add job to the context
        return context

    def perform_create(self, serializer):
        # Get the logged-in user and their profile
        user = self.request.user

        # Check if the user's account_type is 'job_seeker'
        if user.account_type != 'job_seeker':
            raise ValidationError("Only job seekers can apply for jobs.")

        try:
            applicant_profile = user.job_seeker_profile
        except JobSeekerProfile.DoesNotExist:
            raise ValidationError("Only job seekers can apply for jobs.")

        # Ensure the applicant has a resume before saving the application
        if not applicant_profile.resume_url:
            raise ValidationError(
                "You must have a resume to apply for this job.")

          # Get the job object from the URL (ensure it exists)
        job = self.get_serializer_context()['job']

        # Save the application with applicant and job details
        serializer.save(applicant=applicant_profile, job=job,
                        resume_url=applicant_profile.resume_url)


class JobApplicationStatusView(APIView):
    # Only authenticated users can access
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # Ensure the user is a job seeker
        user = request.user
        if user.account_type != 'job_seeker':
            raise PermissionDenied(
                "Only job seekers can check application status.")

        # Check if the job exists
        try:
            job = Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise NotFound("The job you're trying to check does not exist.")

        # Check if the user has applied for the job
        try:
            application = JobApplication.objects.get(
                applicant=user.job_seeker_profile, job=job)
            return Response(
                {"status": application.status},
                status=status.HTTP_200_OK
            )
        except JobApplication.DoesNotExist:
            # If no application exists for this user and job, return "Not applied"
            return Response(
                {"status": "Not applied"},
                status=status.HTTP_200_OK
            )

# View to list all jobs applied


class AppliedJobsListView(generics.ListAPIView):
    serializer_class = JobDetailSerializer  # Use the Job serializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        # Get the current user
        user = self.request.user

        # Check if the user's account_type is 'job_seeker'
        if user.account_type != 'job_seeker':
            raise PermissionDenied("Only job seekers can view applied jobs.")

        # Retrieve the JobSeekerProfile for the logged-in user
        seeker_profile = user.job_seeker_profile

        # Retrieve the Job objects related to the jobs the user has applied for
        return Job.objects.filter(applications__applicant=seeker_profile).distinct()


class JobApplicationsView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        job_id = self.kwargs['pk']  # Extract job_id from the URL

        # Fetch the job
        job = get_object_or_404(Job, pk=job_id)

        # Check if the current user's profile is in the JobHirerProfile table
        try:
            hirer_profile = JobHirerProfile.objects.get(
                user=self.request.user.id)
        except JobHirerProfile.DoesNotExist:
            raise PermissionDenied(
                "You do not have a hirer profile to view these applications.")

        # Verify the account_type in the CustomUser table
        user_account_type = CustomUser.objects.get(
            id=self.request.user.id).account_type
        if user_account_type != 'job_hirer':
            raise PermissionDenied(
                "You do not have the correct account type to view these applications.")

         # Ensure that the hirer profile is the one that posted the job
        if job.posted_by.id != hirer_profile.id:
            raise PermissionDenied(
                "You do not have permission to view the applications for this job.")

        # Fetch all job applications associated with the job_id
        applications = JobApplication.objects.filter(job_id=job_id)

        # If no applications are found, return an empty queryset
        return applications

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            # Return a custom response when there are no applications
            return Response(
                {"message": f"No applications"},
                status=status.HTTP_200_OK
            )

        # If applications exist, use the default list method
        serializer = self.get_serializer(queryset, many=True)
        return Response({"applications": serializer.data})

# class JobApplicationsView(generics.RetrieveAPIView):
#     serializer_class = JobApplicationDetailSerializer

#     def get_queryset(self):
#         return Job.objects.all()

#     def get(self, request, *args, **kwargs):
#         job = self.get_object()
#         job_applications, created = JobApplications.objects.get_or_create(job=job)
#         applications = job_applications.applications
#         serializer = self.get_serializer(applications, many=True)
#         return Response(serializer.data)


# View to retrieve, update, and delete a job
# class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Job.objects.all()
#     serializer_class = JobSerializer
#     permission_classes = [IsAuthenticated]  # , IsJobHirerAndOwner

# View to create a job application


# class JobApplicationCreateView(generics.CreateAPIView):
#     queryset = JobApplication.objects.all()
#     permission_classes = [IsAuthenticated]
#     serializer_class = JobApplicationSerializer

#     # Override the perform_create method to create a notification for the job poster
#     def perform_create(self, serializer):
#         job_application = serializer.save(applicant=self.request.user)
#         Notification.objects.create(
#             user=job_application.job.posted_by,
#             message=f'{self.request.user.get_full_name()} has applied for the role {
#                 job_application.job.position}'
#         )

# View to list all job applications for job hirers


# class JobApplicationListView(generics.ListAPIView):
#     queryset = JobApplication.objects.all()
#     serializer_class = JobApplicationSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         if user.account_type == 'job_hirer':
#             return JobApplication.objects.filter(job__posted_by=user)
#         return JobApplication.objects.none()

# # View to list all jobs posted by the authenticated user with filtering and sorting options


# class JobPostedListView(generics.ListAPIView):
#     serializer_class = JobSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = CustomPagination

#     def get_queryset(self):
#         user = self.request.user
#         queryset = Job.objects.filter(posted_by=user)

#         # Filtering by position
#         position = self.request.query_params.get('position', None)
#         if position:
#             queryset = queryset.filter(position__icontains=position)

#         # Filtering by tags
#         tags = self.request.query_params.get('tags', None)
#         if tags:
#             queryset = queryset.filter(tags__icontains=tags)

#         # Filtering by location
#         location = self.request.query_params.get('location', None)
#         if location:
#             queryset = queryset.filter(
#                 location_restriction__icontains=location)

#         # General search
#         search_query = self.request.query_params.get('search', None)
#         if search_query:
#             queryset = queryset.filter(
#                 Q(position__icontains=search_query) | Q(
#                     tags__icontains=search_query)
#             )

#         # Filtering by salary range
#         salary_min = self.request.query_params.get('salary_min', None)
#         salary_max = self.request.query_params.get('salary_max', None)
#         if salary_min and salary_max:
#             queryset = queryset.filter(
#                 Q(annual_salary_min__gte=salary_min) & Q(
#                     annual_salary_max__lte=salary_max)
#             )
#         elif salary_min:
#             queryset = queryset.filter(annual_salary_min__gte=salary_min)
#         elif salary_max:
#             queryset = queryset.filter(annual_salary_max__lte=salary_max)

#         # Sorting
#         sort_by = self.request.query_params.get('sort_by', None)
#         sort_mapping = {
#             'latest': '-created_at',
#             'highest_salary': '-annual_salary_max',
#         }

#         if sort_by:
#             queryset = queryset.order_by(sort_mapping[sort_by])

#         return queryset

#     # Add request to serializer context
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['request'] = self.request
#         return context

# # View to list all job applications made by the authenticated user with filtering and sorting options


# class AppliedJobsView(generics.ListAPIView):
#     serializer_class = JobApplicationSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = CustomPagination

#     def get_queryset(self):
#         user = self.request.user
#         queryset = JobApplication.objects.filter(applicant=user)

#         # Filtering by job position
#         position = self.request.query_params.get('position', None)
#         if position:
#             queryset = queryset.filter(job__position__icontains=position)

#         # Filtering by tags
#         tags = self.request.query_params.get('tags', None)
#         if tags:
#             queryset = queryset.filter(job__tags__icontains=tags)

#         # Filtering by location
#         location = self.request.query_params.get('location', None)
#         if location:
#             queryset = queryset.filter(
#                 job__location_restriction__icontains=location)

#         # General search
#         search_query = self.request.query_params.get('search', None)
#         if search_query:
#             queryset = queryset.filter(
#                 Q(job__position__icontains=search_query) | Q(
#                     job__tags__icontains=search_query)
#             )

#         # Filtering by salary range
#         salary_min = self.request.query_params.get('salary_min', None)
#         salary_max = self.request.query_params.get('salary_max', None)
#         if salary_min and salary_max:
#             queryset = queryset.filter(
#                 Q(job__annual_salary_min__gte=salary_min) & Q(
#                     job__annual_salary_max__lte=salary_max)
#             )
#         elif salary_min:
#             queryset = queryset.filter(job__annual_salary_min__gte=salary_min)
#         elif salary_max:
#             queryset = queryset.filter(job__annual_salary_max__lte=salary_max)

#         # Sorting
#         sort_by = self.request.query_params.get('sort_by', None)
#         sort_mapping = {
#             'latest': '-job__created_at',
#             'highest_salary': '-job__annual_salary_max',
#         }

#         if sort_by:
#             queryset = queryset.order_by(sort_mapping[sort_by])

#         return queryset

#     # Add request to serializer context
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['request'] = self.request
#         return context

# # API view to get unread notifications for the authenticated user


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def notifications(request):
#     notifications = Notification.objects.filter(
#         user=request.user, is_read=False).order_by('-created_at')
#     return Response({'notifications': notifications.values()})

# # API view to mark a notification as read


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def mark_notification_as_read(request, notification_id):
#     try:
#         notification = Notification.objects.get(
#             id=notification_id, user=request.user)
#         notification.is_read = True
#         notification.save()
#         return Response({'status': 'Notification marked as read'})
#     except Notification.DoesNotExist:
#         return Response({'error': 'Notification not found'}, status=404)
