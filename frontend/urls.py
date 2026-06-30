from django.urls import path
from . import views
from calendar_app import views as calendar_views

app_name = 'frontend'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('donate/', views.DonateView.as_view(), name='donate'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('resources/', views.ResourcesView.as_view(), name='resources'),
    path('news/', views.NewsListView.as_view(), name='news'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('events/<int:pk>/register/', calendar_views.register_for_event, name='event_register'),
    path('events/<int:pk>/calendar.ics', calendar_views.event_ics, name='event_ics'),
]
