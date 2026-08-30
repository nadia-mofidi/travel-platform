from django.urls import path,include
from blog.views import *

app_name='blog'
urlpatterns = [
    path("",blog_view, name='index'),
    path("<int:pid>/",blog_single, name='single'),
    path("category/<str:cat_name>/",blog_view,name='category'),
    path("author/<str:auth_username>/",blog_view,name='author'),
    path("search/",blog_search,name='search'),
    path("tags/<str:tag_name>/",blog_view,name='tags'),
    path("dashboard/", author_dashboard, name="dashboard"),

]