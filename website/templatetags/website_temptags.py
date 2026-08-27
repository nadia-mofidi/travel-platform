from django import template
from blog.models import Post
from django.utils import timezone
register = template.Library()


@register.inclusion_tag('website/website-recent-posts.html')
def recentposts():
    posts = Post.objects.filter(status=1).order_by("-publish_date")[:6]
    return {'posts': posts}

