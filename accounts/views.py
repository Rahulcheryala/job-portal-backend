# from rest_framework import generics, permissions
# from rest_framework_simplejwt.views import TokenObtainPairView
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.contrib.auth import get_user_model
# from rest_framework import serializers
# from rest_framework import generics, status
# from rest_framework.response import Response
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_decode
# from django.contrib.auth import get_user_model
# from django.utils.encoding import force_str
# from django.shortcuts import get_object_or_404
# from django.http import HttpResponse
# from django.contrib.auth.hashers import make_password
# from django.core.mail import EmailMessage
# # Importing the serializers from the serializers module
# from .serializers import (
#     JobSeekerRegisterSerializer,
#     JobHirerRegisterSerializer,
#     # CustomTokenObtainPairSerializer,
#     # ProfileSerializer,
#     # PasswordResetRequestSerializer,
#     # ResumeUpdateSerializer,

# )
# CustomUser = get_user_model()   # Retrieve the custom user model

# View for job seeker registration


# class JobSeekerRegisterView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()  # Define the queryset
#     # Allow any user to access this view
#     permission_classes = (permissions.AllowAny,)
#     # Use JobSeekerRegisterSerializer for serialization
#     serializer_class = JobSeekerRegisterSerializer

# View for job hirer registration


# class JobHirerRegisterView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = JobHirerRegisterSerializer

# class CustomTokenObtainPairView(TokenObtainPairView):   # View for obtaining JWT token
#     serializer_class = CustomTokenObtainPairSerializer

# class ProfileView(generics.RetrieveUpdateAPIView):  # View for retrieving and updating profiles
#     queryset = CustomUser.objects.all()
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = ProfileSerializer

#     def get_object(self):  # Retrieve the profile of the current user
#         return self.request.user

# class PasswordResetRequestView(generics.GenericAPIView):  # View for requesting password reset
#     serializer_class = PasswordResetRequestSerializer

#     def post(self, request, *args, **kwargs):  # Handle POST requests
#         serializer = self.get_serializer(data=request.data)  # Deserialize the request data
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"detail": "Password reset e-mail has been sent."}, status=status.HTTP_200_OK)   # Return a success response

# class PasswordResetConfirmSerializer(serializers.Serializer):  # Serializer for confirming password reset
#     new_password = serializers.CharField(write_only=True)   # Define new_password field as write-only

# class PasswordResetConfirmView(generics.GenericAPIView):  # View for confirming password reset
#     serializer_class = PasswordResetConfirmSerializer
#     # Handle POST requests
#     def post(self, request, uidb64, token, *args, **kwargs):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64)) # Decode the UID
#             user = get_object_or_404(CustomUser, pk=uid) # Get the user or return 404
#         except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#             user = None

#         if user is not None and default_token_generator.check_token(user, token):  # Check if user and token are valid
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             user.password = make_password(serializer.validated_data['new_password'])  # Set the new password
#             user.save()
#             return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK) # Return a success response
#         else:
#             return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST) # Return an error response

# def some_view(request):
#     user = request.user
#     if hasattr(user, 'github_access_token'):
#         github_access_token = user.github_access_token
#         # Use the access token as needed
#         ...
#     return render(request, 'some_template.html', {})

# # View for account activation
# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = CustomUser.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):  # Check if user and token are valid
#         user.is_active = True # Activate the user
#         user.save() # Save the user
#         return redirect('http://localhost:3000/login')  # Redirect to frontend login page
#     else:
#         return HttpResponse('Activation link is invalid!') # Return an error response

# # View for retrieving, updating, and deleting resumes
# class ResumeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = ResumeUpdateSerializer # Use ResumeUpdateSerializer for serialization
#     permission_classes = [permissions.IsAuthenticated]
#     # Retrieve the resume of the current user
#     def get_object(self):
#         return self.request.user


from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import transaction
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from .serializers import CustomTokenObtainPairSerializer, FileUploadSerializer, JobSeekerProfileSerializer, JobSeekerRegistrationSerializer, JobHirerRegistrationSerializer, CustomUserDetailSerializer, ProfileSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from .models import CustomUser, JobHirerProfile, JobSeekerProfile, PersonalInfo


# View for job seeker registration
class JobSeekerRegisterView(generics.CreateAPIView):
    serializer_class = JobSeekerRegistrationSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({
                    "message": "Job seeker registered successfully",
                    "user": serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "message": "An error occurred during registration",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for job hirer registration
class JobHirerRegisterView(generics.CreateAPIView):
    serializer_class = JobHirerRegistrationSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({
                    "message": "Job hirer registered successfully",
                    "user": serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "message": "An error occurred during registration",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for obtaining JWT token
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# View for retrieving user details
class CustomUserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()  # Fetch all users
    serializer_class = CustomUserDetailSerializer
    # Ensure only authenticated users can access the view
    permission_classes = [IsAuthenticated]

    # Use the currently authenticated user as the target for fetching the details
    def get_object(self):
        return self.request.user


# View for retrieving and updating profiles
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


# View for requesting password reset
class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):  # Handle POST requests
        # Deserialize the request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Return a success response
        return Response({"detail": "Password reset link has been sent."}, status=status.HTTP_200_OK)


# View for confirming password reset
class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    # Handle POST request
    def post(self, request, uidb64, token, *args, **kwargs):
        # Pass the token and uidb64 to the serializer via the context
        serializer = self.get_serializer(data=request.data,
                                         context={'uidb64': uidb64, 'token': token})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)


class ProfilePictureUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            # Call the method to upload the file to S3
            s3_file_url = serializer.upload_file_to_s3()

            # Update the user's profile with the new file URL
            user = request.user
            user.profile_picture_url = s3_file_url
            user.save()

            return Response({
                'message': 'File uploaded successfully!',
                'profile_picture_url': s3_file_url
            }, status=status.HTTP_200_OK)

        return Response({'message': 'No file uploaded or invalid file.'}, status=status.HTTP_400_BAD_REQUEST)


class ResumeUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        # Check if the user is a job seeker
        if request.user.account_type != 'job_seeker':
            return Response({'error': 'User must be a job seeker to upload a resume.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            # Call the method to upload the file to S3
            s3_file_url = serializer.upload_file_to_s3()

            # Update the resume_url in the JobSeekerProfile model
            job_seeker_profile = JobSeekerProfile.objects.get(
                user=request.user)
            job_seeker_profile.resume_url = s3_file_url
            job_seeker_profile.save()

            return Response({
                'message': 'Resume uploaded successfully!',
                'resume_url': s3_file_url
            }, status=status.HTTP_200_OK)

        return Response({'message': 'No file uploaded or invalid file.'}, status=status.HTTP_400_BAD_REQUEST)


class CompanyPhotoUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        # Check if the user is a job hirer
        if request.user.account_type != 'job_hirer':
            return Response({'error': 'User must be a job hirer to upload a company logo.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            # Call the method to upload the file to S3
            s3_file_url = serializer.upload_file_to_s3()

            # Update the company_logo_url in the JobHirerProfile model
            job_hirer_profile = JobHirerProfile.objects.get(user=request.user)
            job_hirer_profile.company_photo_url = s3_file_url
            job_hirer_profile.save()

            return Response({
                'message': 'Company logo uploaded successfully!',
                'company_photo_url': s3_file_url
            }, status=status.HTTP_200_OK)

        return Response({'message': 'No file uploaded or invalid file.'}, status=status.HTTP_400_BAD_REQUEST)


class CompanyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Check if the user is a job hirer
        if request.user.account_type != 'job_hirer':
            return Response(
                {'error': 'User must be a job hirer to access company information.'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            # Fetch the JobHirerProfile associated with the user
            job_hirer_profile = JobHirerProfile.objects.get(user=request.user)

            # Prepare the response data
            company_data = {
                'company_name': job_hirer_profile.company_name,
                'company_photo_url': job_hirer_profile.company_photo_url,
                'company_website': job_hirer_profile.company_website,
            }

            return Response(company_data, status=status.HTTP_200_OK)

        except JobHirerProfile.DoesNotExist:
            return Response(
                {'error': 'Job hirer profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class JobSeekerProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSeekerProfileSerializer

    def get_object(self):
        # Get the current user
        user = self.request.user

        # Ensure the user has a JobSeekerProfile
        if not hasattr(user, 'job_seeker_profile'):
            raise Http404("Job Seeker Profile does not exist.")

        return user.job_seeker_profile

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


@csrf_exempt
def activate(request, uidb64, token):
    print(f"UID: {uidb64}, Token: {token}")  # Debugging line
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(CustomUser, pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        print("User activated")  # Debugging line
        user.save()
        # return HttpResponse('Account activated successfully!')
        return redirect(f"{settings.BASE_FRONTEND_URL}/login")
    else:
        return HttpResponse('Activation link is invalid!')
