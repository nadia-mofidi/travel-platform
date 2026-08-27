from django.contrib import admin
from blog.models import Post,Category,Comment
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class PostAdmin(SummernoteModelAdmin):
    date_hierarchy='create_date'
    empty_value_display='-empty-'
    list_display=('id','title','author','counted_views','status','login_require','publish_date','create_date','update_date')
    list_filter=('status','author')
   # ordering=["-create_date"]#minus befor field name makes it descending
    search_fields=['title' ,'content']
    summernote_fields = ('content',)

class CommentAdmin(admin.ModelAdmin):
    date_hierarchy='create_date'
    empty_value_display='-empty-'
    list_display=('id','name','post','approved','create_date')
    list_filter=('approved','post')

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Comment,CommentAdmin)