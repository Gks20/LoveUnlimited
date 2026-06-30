from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from frontend.models import Post


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return [
            'frontend:home',
            'frontend:about',
            'frontend:contact',
            'frontend:donate',
            'frontend:calendar',
            'frontend:resources',
            'frontend:news',
        ]

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Post.objects.filter(is_published=True, published_at__lte=timezone.now())

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('frontend:news_detail', kwargs={'slug': obj.slug})
