from django.contrib import admin
from django.db import models
from .models import ResourceCategory, Resource, SiteContent, Post, DonationSettings, TeamMember


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "ordering")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("ordering", "name")


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "phone", "website", "is_active", "ordering")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description", "address", "phone", "website")
    ordering = ("category__ordering", "ordering", "name")


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('key', 'language', 'title', 'preview')
    list_filter = ('language', 'key')
    search_fields = ('key', 'title', 'body')
    ordering = ('key', 'language')
    formfield_overrides = {
        models.TextField: {'widget': admin.widgets.AdminTextareaWidget(attrs={'rows': 8, 'cols': 80})},
    }

    @admin.display(description='Preview')
    def preview(self, obj):
        return (obj.body[:60] + '…') if len(obj.body) > 60 else obj.body


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'ordering', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('ordering', 'is_active')
    search_fields = ('name', 'role', 'bio')
    ordering = ('ordering', 'name')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'is_published', 'published_at')
    list_filter = ('language', 'is_published')
    search_fields = ('title', 'body', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)


@admin.register(DonationSettings)
class DonationSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Zeffy', {'fields': ('zeffy_form_link', 'zeffy_embed_html')}),
        ('Copy', {'fields': ('tax_id', 'impact_25', 'impact_50', 'impact_100')}),
    )

    def has_add_permission(self, request):
        return not DonationSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
