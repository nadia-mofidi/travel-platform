from django import template
from blog.models import Post
from django.utils import timezone
register = template.Library()


@register.inclusion_tag('website/website-recent-posts.html')
def recentposts():
    posts = Post.objects.filter(status=True,
    publish_date__lte=timezone.now()).order_by("-publish_date")[:6]
    return {'posts': posts}

@register.inclusion_tag('website/website-featured-posts.html')
def featuredposts():
    featured_posts = Post.objects.filter(status=True,
    is_featured=True,
    publish_date__lte=timezone.now()).order_by('-publish_date')[:4]
    return {'posts': featured_posts}