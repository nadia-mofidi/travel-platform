from django.contrib import admin
from website.models import Contact,Newsletter
# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    date_hierarchy='create_date'
    empty_value_display='-empty-'
    list_display=('name','subject','email','create_date','update_date')
    list_filter=('email',)
    search_fields=['name','massage']
admin.site.register(Contact,ContactAdmin)



admin.site.register(Newsletter)