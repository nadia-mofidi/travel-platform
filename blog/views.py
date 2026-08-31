from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from blog.models import Post,Comment
from django.db.models import F,Q
from django.core.paginator import Paginator
from blog.forms import CommentForm,PostForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.decorators import author_required

def blog_view (request,cat_name=None,auth_username=None,**kwargs):

    posts=Post.objects.filter(status=1,publish_date__lte=timezone.now()).order_by('-publish_date')
    if cat_name:
        posts = posts.filter(category__name = cat_name)
    author = None
    if auth_username:
        posts = posts.filter(author__username = auth_username)
        author = get_object_or_404(User,username=auth_username)
    if kwargs.get('tag_name'):
        posts = posts.filter(tags__name = kwargs['tag_name'])

    paginator = Paginator(posts,2)
    page_number=request.GET.get('page')
    posts = paginator.get_page(page_number)
   
    context={'posts':posts,'author':author}
    return render(request,"blog/blog-home.html",context)

def blog_single (request,pid):
    
    post = get_object_or_404(Post, pk=pid, status=True, publish_date__lte=timezone.now())
    if post.login_require==True and not request.user.is_authenticated:
        return redirect('accounts:login')
    #-----------
    published_posts=Post.objects.filter(status=True,publish_date__lte=timezone.now())
    prev_post = published_posts.filter(
    Q(publish_date__lt=post.publish_date) |
    Q(publish_date=post.publish_date, id__lt=post.id)
    ).order_by('-publish_date', '-id').first()

    next_post = published_posts.filter(
    Q(publish_date__gt=post.publish_date) |
    Q(publish_date=post.publish_date, id__gt=post.id)
    ).order_by('publish_date', 'id').first()
    #-------------
    comments = Comment.objects.filter( post=post, approved=True ).order_by("-create_date")

    if request.method=="POST":
        form = CommentForm(request.POST, user=request.user)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            
            if request.user.is_authenticated:
                comment.name = request.user.get_full_name() or request.user.username
                comment.email = request.user.email

            form.save()
            messages.add_message(request,messages.SUCCESS,'Your comment has been submitted and is awaiting approval.')
            
            return redirect('blog:single', pid=post.id)
        else:
            messages.add_message(request,messages.ERROR,'Your comment couldn\'t be submitted')
    else:
        form = CommentForm( user=request.user)

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

@login_required
@author_required
def author_dashboard(request):

    posts = Post.objects.filter(author=request.user)
    context = {'posts': posts,}

    return render(request,'blog/author-dashboard.html',context)

@login_required
@author_required
def create_post(request):

    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)

        if form.is_valid():
            post = form.save(commit=False)

            post.author = request.user
            post.save()

            form.save_m2m()

            return redirect('blog:dashboard')
        
    else:
        form = PostForm()

    context = {'form': form,}

    return render(request,'blog/create-post.html',context)

@login_required
@author_required
def edit_post(request, pid):

    post = get_object_or_404(Post,id=pid,author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES,instance=post)

        if form.is_valid():
            form.save()
            return redirect('blog:dashboard')

    else:
        form = PostForm(instance=post)

    context = {'form': form,'post': post,}

    return render(request,'blog/edit-post.html',context)

@login_required
@author_required
def delete_post(request, pid):
    post = get_object_or_404(Post, id=pid, author=request.user)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:dashboard')

    return render(request, 'blog/delete-post.html', {'post': post})