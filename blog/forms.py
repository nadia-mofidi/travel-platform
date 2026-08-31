from django import forms
from blog.models import Comment,Post
from captcha.fields import CaptchaField
from django_summernote.widgets import SummernoteWidget

class CommentForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            self.fields['name'].required = False
            self.fields['email'].required = False
    class Meta:
        model = Comment
        fields = ["name","email","subject","message",]
        

class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = [
            'title',
            'content',
            'image',
            'category',
            'tags',
            'login_require',
            'publish_date',
            'status',
        ]

        widgets = {
            'content': SummernoteWidget(),
        }