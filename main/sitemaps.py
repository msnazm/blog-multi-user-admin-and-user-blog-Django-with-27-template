from django.contrib.sitemaps import Sitemap
from main.models import Product

class ProductSitemap(Sitemap):
    changefreq = "weekly" 
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.create_date