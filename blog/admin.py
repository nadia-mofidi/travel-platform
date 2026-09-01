from django.contrib import admin
from blog.models import Post,Category,Comment
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.auth.models import User
# Register your models here.

class PostAdmin(SummernoteModelAdmin):
    date_hierarchy='create_date'
    empty_value_display='-empty-'
    list_display=('id','title','author','counted_views','status','is_featured','login_require','publish_date','create_date','update_date')
    list_filter=('status','author', 'is_featured')
   # ordering=["-create_date"]#minus befor field name makes it descending
    search_fields=['title' ,'content']
    summernote_fields = ('content',)
    list_display_links = ('id','title','author')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(
                groups__name="Authors"
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class CommentAdmin(admin.ModelAdmin):
    date_hierarchy='create_date'
    empty_value_display='-empty-'
    list_display=('id','name','post','approved','create_date')
    list_filter=('approved','post')

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Comment,CommentAdmin)