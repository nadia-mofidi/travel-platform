from django.contrib.sitemaps import Sitemap
from blog.models import Post

class BlogSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return Post.objects.filter(status=True)
    def lastmod(self,obj):
        return obj.publish_date