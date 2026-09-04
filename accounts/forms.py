from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
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
        fields = ['username','first_name', 'last_name', 'email']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].disabled = True

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'job_title',
            'bio',
            'avatar',
            'avatar_preset',
            'facebook',
            'twitter',
            'instagram',
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
                'instagram',
                'behance',
            ]

            for field in author_fields:
                self.fields.pop(field)

    def clean_avatar_preset(self):
        avatar_preset = self.cleaned_data.get('avatar_preset')
    
        allowed_presets = [
            'avatar1.png',
            'avatar2.png',
            'avatar3.png',
            'avatar4.png',
            'avatar5.png',
            'avatar6.png',
        ]
    
        if avatar_preset and avatar_preset not in allowed_presets:
            raise forms.ValidationError('Invalid avatar selection.')
    
        return avatar_preset