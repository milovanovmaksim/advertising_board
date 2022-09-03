from django.contrib.sitemaps import Sitemap

from .models import Ad


class MainSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Ad.objects.all()

    def lastmod(self, obj):
        return obj.created_at


