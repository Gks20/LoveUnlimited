from django.contrib.sitemaps import Sitemap
from django.urls import reverse


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
        ]

    def location(self, item):
        return reverse(item)
