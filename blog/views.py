from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from blog.models import Post,Comment
from django.db.models import F
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger,InvalidPage
from blog.forms import CommentForm
from django.contrib import messages
from django.contrib.auth.models import User

def blog_view (request,cat_name=None,auth_username=None,**kwargs):

    posts=Post.objects.filter(publish_date__lte=timezone.now()).reverse()
    for post in posts:
        post.status=1
        post.save()
    if cat_name:
        posts = posts.filter(category__name = cat_name)
    author = None
    if auth_username:
        posts = posts.filter(author__username = auth_username)
        author = User.objects.get(username=auth_username)
    if kwargs.get('tag_name'):
        posts = posts.filter(tags__name = kwargs['tag_name'])

    posts = Paginator(posts,2)
    try:
        page_number=request.GET.get('page')
        posts = posts.page(page_number)# یا به جای همه اکسپت ها از گت پیج در همین خط استفاده کن
    except PageNotAnInteger:
        posts = posts.page(1)
    except EmptyPage:
        posts = posts.page(1)
    except InvalidPage:
        posts = posts.page(1)
    context={'posts':posts,'author':author}
    return render(request,"blog/blog-home.html",context)

def blog_single (request,pid):
    
    post = get_object_or_404(Post, pk=pid,status=1)
    if post.login_require==True and not request.user.is_authenticated:
        return redirect('accounts:login')
    #-----------
    posts=Post.objects.filter(status=1)
    posts=list(posts)
    current_index=posts.index(post)
    if current_index>0:
        prev_post=posts[current_index-1] 
    else: 
        prev_post=None 
    if current_index<len(posts)-1:
        next_post=posts[current_index+1]
    else:
        next_post=None
    #-------------
    comments = Comment.objects.filter( post=post, approved=True ).order_by("-create_date")

    if request.method=="POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Your comment is submitted successfully')
        else:
            messages.add_message(request,messages.ERROR,'Your comment couldn\'t be submitted')

    form = CommentForm()
    context = {'post': post,"next_post":next_post,
               "prev_post":prev_post,"comments":comments,'form':form}  
    # افزایش تعداد بازدید
    post.counted_views = F('counted_views') + 1
    post.save(update_fields=['counted_views'])
    post.refresh_from_db()

    return render(request,"blog/blog-single.html",context)

def blog_search(request):
    posts=Post.objects.filter(status=1)
    if request.method=='GET':
        if s:=request.GET.get('s'):
            posts = posts.filter(content__iregex=rf"\b{s}\b")#__contains
    
    context={'posts':posts}
    return render(request,"blog/blog-home.html",context)

def test_view(request):
    # post=Post.objects.get(id=pid)

    return render(request,"test.html")
