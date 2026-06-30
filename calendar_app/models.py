from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code")
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Event Categories"
    
    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200, blank=True)
    is_public = models.BooleanField(default=True, help_text="Show on public calendar")
    max_attendees = models.IntegerField(null=True, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['date', 'start_time']
    
    def __str__(self):
        return f"{self.title} - {self.date}"
    
    @property
    def is_upcoming(self):
        return self.date >= timezone.now().date()
    
    @property
    def duration_hours(self):
        start_dt = timezone.datetime.combine(self.date, self.start_time)
        end_dt = timezone.datetime.combine(self.date, self.end_time)
        duration = end_dt - start_dt
        return duration.total_seconds() / 3600

    @property
    def registration_count(self):
        return self.eventregistration_set.count()

    @property
    def is_full(self):
        if self.max_attendees is None:
            return False
        return self.registration_count >= self.max_attendees


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'email']
        ordering = ['registered_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event.title}"
