# # accounts/forms.py
# from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import CustomUser

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'date_of_birth', 'email', 'phone_number', 'number_of_experiences', 'password1', 'password2')

# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'date_of_birth', 'phone_number', 'number_of_experiences', 'profile_pic', 'bio', 'social_media')

# class LoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, JobSeekerProfile, JobHirerProfile


class CustomUserCreationForm(UserCreationForm):
    # Fields specific to job seekers and hirers
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Basic user fields that are required for both job seekers and job hirers
        fields = ('username', 'first_name', 'last_name', 'email',
                  'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()

        # Save job seeker or job hirer profile based on account_type
        account_type = self.cleaned_data.get('account_type')

        if account_type == 'job_seeker':
            JobSeekerProfile.objects.create(
                user=user,
                years_of_experience=self.cleaned_data.get(
                    'years_of_experience'),
                technical_skills=self.cleaned_data.get('technical_skills'),
                location=self.cleaned_data.get('location'),
            )
        elif account_type == 'job_hirer':
            JobHirerProfile.objects.create(
                user=user,
                working_email=self.cleaned_data.get('working_email'),
                looking_for=self.cleaned_data.get('looking_for'),
            )

        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()

        # Update job seeker or job hirer profile based on account_type
        account_type = user.account_type
        if account_type == 'job_seeker' and hasattr(user, 'job_seeker_profile'):
            seeker_profile = user.job_seeker_profile
            seeker_profile.years_of_experience = self.cleaned_data.get(
                'years_of_experience')
            seeker_profile.technical_skills = self.cleaned_data.get(
                'technical_skills')
            seeker_profile.location = self.cleaned_data.get('location')
            seeker_profile.save()

        elif account_type == 'job_hirer' and hasattr(user, 'job_hirer_profile'):
            hirer_profile = user.job_hirer_profile
            hirer_profile.working_email = self.cleaned_data.get(
                'working_email')
            hirer_profile.looking_for = self.cleaned_data.get('looking_for')
            hirer_profile.save()

        return user


# Updated LoginForm to use `username` and `password`
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class FileUploadForm(forms.Form):
    image = forms.ImageField(required=False)
    pdf = forms.FileField(required=False)
