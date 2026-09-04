from django.test import TestCase
from .forms import ProfileForm
# Create your tests here.



class ProfileFormTest(TestCase):

    def test_valid_avatar_preset(self):
        form = ProfileForm(data={
            'avatar_preset': 'avatar3.png',
        })

        self.assertTrue(form.is_valid())

    def test_invalid_avatar_preset(self):
        form = ProfileForm(data={
            'avatar_preset': 'hacker.png',
        })

        self.assertFalse(form.is_valid())