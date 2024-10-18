from django.urls import path, include
# Import TokenRefreshView for handling JWT token refresh
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
# Import static to serve static and media files during development
from django.conf.urls.static import static

# Import views from the current app
from .views import (
    CompanyPhotoUploadView,
    CompanyProfileView,
    JobSeekerProfileView,
    JobSeekerRegisterView,
    JobHirerRegisterView,
    CustomTokenObtainPairView,
    CustomUserDetailView,
    ProfilePictureUploadView,
    ProfileView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ResumeUploadView,
    activate,
)

# Define URL patterns for the application
urlpatterns = [
    # URL pattern for job seeker registration
    path('register/job-seeker/', JobSeekerRegisterView.as_view(),
         name='job_seeker_register'),
    # URL pattern for job hirer registration
    path('register/job-hirer/', JobHirerRegisterView.as_view(),
         name='job_hirer_register'),
    # URL pattern for account activation
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    # URL pattern for user login
    path('login/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    # URL pattern for requesting password reset
    path('reset-password/', PasswordResetRequestView.as_view(),
         name='password_reset_request'),
    # URL pattern for confirming password reset
    path('reset-password/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # URL pattern for basic user details
    path('user-details/', CustomUserDetailView.as_view(), name='user_details'),
    # URL pattern for retrieving and updating profiles
    path('profile/', ProfileView.as_view(), name='profile'),
    # URL pattern for uploading profile pictures
    path('upload/profile-picture/',
         ProfilePictureUploadView.as_view(), name='upload_file'),
    # URL pattern for uploading resumes
    path('upload/resume/', ResumeUploadView.as_view(), name='upload_resume'),
    # URL pattern for uploading company photos
    path('upload/company-photo/', CompanyPhotoUploadView.as_view(),
         name='company-photo-upload'),

    path('company-profile/', CompanyProfileView.as_view(), name='company-profile'),
    path('job-seeker-profile/', JobSeekerProfileView.as_view(),
         name='job_seeker_profile'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
