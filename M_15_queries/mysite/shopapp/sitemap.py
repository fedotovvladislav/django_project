from django.contrib.sitemaps import Sitemap

from .models import Product


class ProductSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Product.objects.filter(archived=False).order_by('-created_at')

    def lastmod(self, obj: Product):
        return obj.created_at

