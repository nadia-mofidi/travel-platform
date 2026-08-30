from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )




class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'job_title',
            'bio',
            'avatar',
            'facebook',
            'twitter',
            'github',
            'behance',
        ]

    def __init__(self, *args, is_author=False, **kwargs):
        super().__init__(*args, **kwargs)

        if not is_author:
            author_fields = [
                'job_title',
                'bio',
                'facebook',
                'twitter',
                'github',
                'behance',
            ]

            for field in author_fields:
                self.fields.pop(field)