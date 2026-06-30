from django.urls import path

from . import views

app_name = 'staff_portal'

urlpatterns = [
    path('login/', views.StaffLoginView.as_view(), name='login'),
    path('logout/', views.StaffLogoutView.as_view(), name='logout'),
    path('', views.DashboardView.as_view(), name='dashboard'),

    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/new/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_edit'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),

    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/new/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    path('content/', views.ContentListView.as_view(), name='content_list'),
    path('content/new/', views.ContentCreateView.as_view(), name='content_create'),
    path('content/<int:pk>/edit/', views.ContentUpdateView.as_view(), name='content_edit'),

    path('team/', views.TeamListView.as_view(), name='team_list'),
    path('team/new/', views.TeamCreateView.as_view(), name='team_create'),
    path('team/<int:pk>/edit/', views.TeamUpdateView.as_view(), name='team_edit'),
    path('team/<int:pk>/delete/', views.TeamDeleteView.as_view(), name='team_delete'),

    path('resources/', views.ResourceListView.as_view(), name='resource_list'),
    path('resources/new/', views.ResourceCreateView.as_view(), name='resource_create'),
    path('resources/<int:pk>/edit/', views.ResourceUpdateView.as_view(), name='resource_edit'),
    path('resources/<int:pk>/delete/', views.ResourceDeleteView.as_view(), name='resource_delete'),

    path('settings/donations/', views.DonationSettingsView.as_view(), name='donation_settings'),
]
