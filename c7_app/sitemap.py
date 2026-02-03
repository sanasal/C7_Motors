from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from c7_app.models import Car, Article

class HomeSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return ['home']

    def location(self, item):
        return reverse('c7_motors:home')


class InventorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return ['inventory']

    def location(self, item):
        return reverse('c7_motors:inventory')

class CarDetailSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.95
    
    def items(self):
        return Car.objects.filter(
            selled=False,
            not_available=False
        ).only('slug')

    def lastmod(self, obj):
        # الأفضل لو عندك updated_at
        return getattr(obj, "updated_at", None)

    def location(self, obj):
        return reverse(
            'c7_motors:car_details',
            args=[obj.slug]
        )

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return [
            'c7_motors:about',
            'c7_motors:contact_us',
            'c7_motors:financing',
        ]

    def location(self, item):
        return reverse(item)

class ArticlesSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Article.objects.only('slug')

    def lastmod(self, obj):
        return getattr(obj, "updated_at", None)

    def location(self, obj):
        return reverse(
            'c7_motors:article_detail',
            args=[obj.slug]
        )
