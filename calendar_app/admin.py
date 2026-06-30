from django.contrib import admin
from .models import EventCategory, Event, EventRegistration


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    search_fields = ['name']


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ['registered_at']
    fields = ['first_name', 'last_name', 'email', 'phone', 'registered_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'start_time', 'location', 'is_public', 'max_attendees', 'registration_count_display']
    list_filter = ['is_public', 'category', 'date']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'date'
    readonly_fields = ['created_at']
    inlines = [EventRegistrationInline]

    @admin.display(description='Registrations')
    def registration_count_display(self, obj):
        return obj.registration_count

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'event', 'registered_at']
    list_filter = ['event', 'registered_at']
    search_fields = ['first_name', 'last_name', 'email', 'event__title']
    readonly_fields = ['registered_at']