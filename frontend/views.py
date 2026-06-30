from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from calendar_app.models import Event
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ContactForm
from .models import ResourceCategory, Resource, Post, SiteContent, DonationSettings


class HomeView(TemplateView):
    template_name = 'frontend/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get upcoming events for the homepage
        upcoming_events = Event.objects.filter(
            date__gte=timezone.now().date()
        ).select_related('category').order_by('date')[:3]
        lang = get_language() or 'en'
        context['upcoming_events'] = upcoming_events
        context['latest_posts'] = Post.objects.filter(
            is_published=True, language=lang
        ).order_by('-published_at')[:3]
        return context


class AboutView(TemplateView):
    template_name = 'frontend/about.html'

    def get_context_data(self, **kwargs):
        from .models import TeamMember
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.filter(is_active=True)
        return context


class ContactView(FormView):
    template_name = 'frontend/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('frontend:contact')

    def form_valid(self, form):
        data = form.cleaned_data
        subject_map = dict(form.fields['subject'].choices)
        subject_label = subject_map.get(data['subject'], data['subject'])
        subject = f"{settings.EMAIL_SUBJECT_PREFIX}Contact: {subject_label} - {data['first_name']} {data['last_name']}"
        body_lines = [
            f"Name: {data['first_name']} {data['last_name']}",
            f"Email: {data['email']}",
            f"Phone: {data.get('phone') or 'N/A'}",
            f"Topic: {subject_label}",
            "",
            "Message:",
            data['message'],
        ]
        body = "\n".join(body_lines)

        # Determine recipients: CONTACT_RECIPIENTS > ADMINS > DEFAULT_FROM_EMAIL
        recipients = getattr(settings, 'CONTACT_RECIPIENTS', []) or [e for _, e in getattr(settings, 'ADMINS', [])]
        if not recipients:
            recipients = [settings.DEFAULT_FROM_EMAIL]
        send_failed = False
        if settings.EMAIL_FEATURE_ENABLED:
            try:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipients,
                    fail_silently=False,
                    reply_to=[data['email']],
                )
            except Exception:
                send_failed = True
            if send_failed:
                messages.error(self.request, "We couldn't send your message right now. Please try again later.")
            else:
                messages.success(self.request, "Thank you! Your message has been received. We'll respond soon.")
        else:
            messages.info(self.request, "Message received (email delivery not yet configured).")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below and resubmit.")
        return super().form_invalid(form)


@method_decorator(cache_page(3600), name='dispatch')  # 1 hour
class DonateView(TemplateView):
    template_name = 'frontend/donate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donation_settings'] = DonationSettings.load()
        return context


@method_decorator(cache_page(600), name='dispatch')  # 10 min; events may update during day
class CalendarView(TemplateView):
    template_name = 'frontend/calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.utils import timezone
        today = timezone.now().date()
        base_qs = Event.objects.filter(is_public=True).select_related('category')
        context['upcoming_events'] = base_qs.filter(date__gte=today).order_by('date', 'start_time')
        context['past_events'] = base_qs.filter(date__lt=today).order_by('-date', '-start_time')
        context['registration_modal'] = self.request.session.pop(
            'event_registration_modal', None
        )
        return context


@method_decorator(cache_page(1800), name='dispatch')  # 30 min for resources page
class ResourcesView(TemplateView):
    template_name = 'frontend/resources.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '').strip()
        category_slug = self.request.GET.get('category')
        categories = ResourceCategory.objects.all()
        resources_qs = Resource.objects.filter(is_active=True).select_related('category')
        if category_slug:
            resources_qs = resources_qs.filter(category__slug=category_slug)
        if q:
            resources_qs = resources_qs.filter(
                models.Q(name__icontains=q) |
                models.Q(description__icontains=q) |
                models.Q(address__icontains=q) |
                models.Q(phone__icontains=q) |
                models.Q(tags__icontains=q) |
                models.Q(category__name__icontains=q)
            )
        # Group resources by category
        grouped = {}
        for cat in categories:
            grouped[cat] = []
        for r in resources_qs:
            grouped[r.category].append(r)
        context.update({
            'query': q,
            'selected_category': category_slug,
            'categories': categories,
            'grouped_resources': grouped,
            'total_results': resources_qs.count(),
        })
        return context


class NewsListView(ListView):
    model = Post
    template_name = 'frontend/news_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        lang = get_language() or 'en'
        return Post.objects.filter(is_published=True, language=lang).order_by('-published_at')


class NewsDetailView(DetailView):
    model = Post
    template_name = 'frontend/news_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        lang = get_language() or 'en'
        return Post.objects.filter(is_published=True, language=lang)
