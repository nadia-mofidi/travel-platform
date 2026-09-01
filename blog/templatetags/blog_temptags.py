from django import template
from blog.models import Post,Category,Comment
from django.utils import timezone
register = template.Library()

@register.inclusion_tag('blog/blog-popular-post.html')
def popularposts():
    posts = Post.objects.filter(status=1,publish_date__lte=timezone.now()).order_by("-counted_views")[:4]
    return {'posts': posts}

@register.inclusion_tag('blog/blog-post-categories.html')
def postcategories():
    posts = Post.objects.filter(status=1,publish_date__lte=timezone.now())
    categories=Category.objects.all()
    cat_dict={}
    for cat in categories:
        cat_dict[cat]=posts.filter(category=cat).count()
    return {'categories':cat_dict}

# @register.simple_tag(name='comments_count')
# def function(pid):
#     cmcount=Comment.objects.filter(post=pid,approved=True).count()
#     return cmcount