from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="blog/",default="blog/default.jpg")#در پوشه مدیا فولدری به نام بلاگ ایجاد میکند
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    tags = TaggableManager()
    category = models.ManyToManyField(Category,)
    counted_views = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    login_require = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["publish_date",]
        # verbose_name="پست"
        # verbose_name_plural="پست ها"
    def __str__(self):
        return f"{self.id}-{self.title}"
    def get_absolute_url(self):
        return reverse("blog:single", kwargs={"pid": self.id})
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    approved = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"cm:{self.id}|{self.post}"
