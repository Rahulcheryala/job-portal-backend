
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    AppliedJobsListView,
    JobApplicationStatusView,
    JobApplicationsView,
    JobApplyView,
    JobCreateView,
    JobDeleteView,
    JobListView,
    JobUpdateView,
    PostedJobsListView,
    # AppliedJobsView,
    JobDetailsView,
    # notifications,
    # mark_notification_as_read,
    # initiate_payment,
    # payment_webhook
)  # Import necessary views from the current app

urlpatterns = [
    # URL for listing jobs
    path('jobs/', JobListView.as_view(), name='job_list'),
    # URL for creating a new job
    path('jobs/create/', JobCreateView.as_view(), name='job_create'),

    # URL for listing jobs the current user has applied to
    path('applied-jobs/', AppliedJobsListView.as_view(), name='applied-jobs'),
    # URL for applying to a job
    path('jobs/<int:pk>/apply/', JobApplyView.as_view(), name='job_apply'),
    # URL for viewing a job application status
    path('jobs/<int:pk>/application-status/',
         JobApplicationStatusView.as_view(), name='job_application_status'),

    # URL for listing job applications
    path('jobs/<int:pk>/applications/',
         JobApplicationsView.as_view(), name='job-applications'),

    # URL for listing jobs posted by the current user
    path('posted-jobs/', PostedJobsListView.as_view(), name='job-posted-list'),
    # # URL for viewing a job's details
    path('jobs/<int:pk>/', JobDetailsView.as_view(), name='job-detail'),
    # URL for updating a job's details
    path('jobs/<int:pk>/update/', JobUpdateView.as_view(), name='job-update'),
    # URL for deleting a job
    path('jobs/<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),

    # path('notifications/read/<int:notification_id>/', mark_notification_as_read,
    #      name='mark_notification_as_read'),  # URL for marking a notification as read
    # # URL for viewing notifications
    # path('notifications/', notifications, name='notifications'),
    # # URL for initiating a payment
    # path('payments/initiate/', initiate_payment, name='initiate-payment'),
    # # URL for handling payment webhooks
    # path('payments/webhook/', payment_webhook, name='payment-webhook'),
]

# If in debug mode, serve media files through Django
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
