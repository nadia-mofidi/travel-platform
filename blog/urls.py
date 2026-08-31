from django.urls import path,include
from blog.views import *

app_name='blog'
urlpatterns = [
    path("",blog_view, name='index'),
    path("category/<str:cat_name>/",blog_view,name='category'),
    path("author/<str:auth_username>/",blog_view,name='author'),
    path("tags/<str:tag_name>/",blog_view,name='tags'),
    path("<int:pid>/",blog_single, name='single'),
    path("search/",blog_search,name='search'),
    
    path("dashboard/", author_dashboard, name="dashboard"),
    path("dashboard/create/",create_post,name="create_post"),
    path("dashboard/<int:pid>/edit/", edit_post, name="edit_post"),
]