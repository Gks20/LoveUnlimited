from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.utils import translation
from django.views import View
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView,
)

from calendar_app.models import Event, EventRegistration, EventCategory
from frontend.models import (
    SiteContent, TeamMember, Resource, ResourceCategory, DonationSettings, HomepageSettings,
)
from .forms import (
    EventForm, SiteContentForm, SiteContentCreateForm, TeamMemberForm,
    ResourceForm, ResourceCategoryForm, DonationSettingsForm, EventCategoryForm,
    HomepageSettingsForm,
)
from staff_portal.content_labels import CONTENT_SECTIONS, CONTENT_LABELS
from staff_portal.content_format import PLAIN_TEXT_KEYS, SINGLE_LINE_KEYS
from staff_portal.content_registry import PREVIEW_PAGES, all_content_keys, build_preview_context
from staff_portal.rich_text import sanitize_html
from .mixins import StaffRequiredMixin, StaffLoginView, StaffLogoutView


class DashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'staff_portal/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['stats'] = {
            'upcoming_events': Event.objects.filter(date__gte=timezone.now().date()).count(),
            'registrations': EventRegistration.objects.filter(
                event__date__gte=timezone.now().date()
            ).count(),
            'resources': Resource.objects.filter(is_active=True).count(),
        }
        ctx['recent_registrations'] = EventRegistration.objects.select_related('event').order_by('-registered_at')[:5]
        ctx['upcoming_events'] = Event.objects.filter(
            date__gte=timezone.now().date()
        ).order_by('date')[:5]
        return ctx


# --- Events ---

class EventListView(StaffRequiredMixin, ListView):
    model = Event
    template_name = 'staff_portal/events/list.html'
    context_object_name = 'events'
    paginate_by = 20

    def get_queryset(self):
        return Event.objects.select_related('category').annotate(
            reg_count=Count('eventregistration')
        ).order_by('-date')


class EventCreateView(StaffRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'staff_portal/events/form.html'
    success_url = reverse_lazy('staff_portal:event_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Your event has been saved and is on the calendar.')
        return super().form_valid(form)


class EventUpdateView(StaffRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'staff_portal/events/form.html'
    success_url = reverse_lazy('staff_portal:event_list')

    def form_valid(self, form):
        messages.success(self.request, 'Your changes to this event have been saved.')
        return super().form_valid(form)


class EventDeleteView(StaffRequiredMixin, DeleteView):
    model = Event
    template_name = 'staff_portal/confirm_delete.html'
    success_url = reverse_lazy('staff_portal:event_list')
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cancel_url'] = reverse('staff_portal:event_list')
        ctx['object_label'] = 'event'
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'The event has been removed.')
        return super().form_valid(form)


class EventDetailView(StaffRequiredMixin, DetailView):
    model = Event
    template_name = 'staff_portal/events/detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['registrations'] = self.object.eventregistration_set.order_by('-registered_at')
        return ctx


# --- Site content ---

class ContentVisualEditorView(StaffRequiredMixin, TemplateView):
    template_name = 'staff_portal/content/visual_editor.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 'home')
        if page not in PREVIEW_PAGES:
            page = 'home'
        lang = self.request.GET.get('lang', 'en')
        if lang not in ('en', 'es'):
            lang = 'en'
        ctx['current_page'] = page
        ctx['current_lang'] = lang
        ctx['preview_pages'] = PREVIEW_PAGES
        ctx['frame_url'] = reverse(
            'staff_portal:content_preview_frame',
            kwargs={'page': page},
        ) + f'?lang={lang}'
        return ctx


@method_decorator(xframe_options_sameorigin, name='dispatch')
class ContentPreviewFrameView(StaffRequiredMixin, TemplateView):
    """Renders a public page inside the visual editor iframe."""

    def get(self, request, page, *args, **kwargs):
        if page not in PREVIEW_PAGES:
            return HttpResponseNotFound()
        lang = request.GET.get('lang', 'en')
        if lang not in ('en', 'es'):
            lang = 'en'
        with translation.override(lang):
            context, _ = build_preview_context(page, request, edit_mode=True)
            context['LANGUAGE_CODE'] = lang
            return render(request, PREVIEW_PAGES[page]['template'], context)


class ContentBlockSaveView(StaffRequiredMixin, View):
    """AJAX endpoint for inline content saves from the visual editor."""

    def post(self, request):
        import json

        try:
            payload = json.loads(request.body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({'ok': False, 'error': 'Invalid request'}, status=400)

        key = (payload.get('key') or '').strip()
        language = (payload.get('language') or 'en').strip()
        body = payload.get('body', '')

        if key not in all_content_keys():
            return JsonResponse({'ok': False, 'error': 'Unknown content block'}, status=400)
        if language not in ('en', 'es'):
            return JsonResponse({'ok': False, 'error': 'Invalid language'}, status=400)

        if key in PLAIN_TEXT_KEYS:
            body = strip_tags(body).strip()
        elif key == 'footer-tagline':
            body = strip_tags(body).strip()
        else:
            body = sanitize_html(body)

        block, _ = SiteContent.objects.update_or_create(
            key=key,
            language=language,
            defaults={
                'title': CONTENT_LABELS.get(key, key.replace('-', ' ').title()),
                'body': body,
            },
        )
        return JsonResponse({
            'ok': True,
            'key': block.key,
            'language': block.language,
            'label': CONTENT_LABELS.get(key, key),
        })


class ContentListView(StaffRequiredMixin, ListView):
    model = SiteContent
    template_name = 'staff_portal/content/list.html'
    context_object_name = 'blocks'
    paginate_by = None

    def get_queryset(self):
        qs = SiteContent.objects.order_by('key', 'language')
        lang = self.request.GET.get('lang', 'en')
        if lang in ('en', 'es'):
            qs = qs.filter(language=lang)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        lang = self.request.GET.get('lang', 'en')
        if lang not in ('en', 'es'):
            lang = 'en'
        ctx['current_lang'] = lang
        blocks_by_key = {b.key: b for b in ctx['blocks']}
        grouped = []
        for section_id, section_title, section_help, items in CONTENT_SECTIONS:
            section_blocks = []
            for key, label in items:
                block = blocks_by_key.get(key)
                if block:
                    section_blocks.append({'block': block, 'label': label})
            if section_blocks:
                grouped.append({
                    'id': section_id,
                    'title': section_title,
                    'help': section_help,
                    'blocks': section_blocks,
                })
        ctx['content_sections'] = grouped
        return ctx


class ContentUpdateView(StaffRequiredMixin, UpdateView):
    model = SiteContent
    form_class = SiteContentForm
    template_name = 'staff_portal/content/form.html'

    def get_success_url(self):
        messages.success(self.request, 'The website text has been updated. Visitors will see your changes right away.')
        return reverse('staff_portal:content_list')


class ContentCreateView(StaffRequiredMixin, CreateView):
    model = SiteContent
    form_class = SiteContentCreateForm
    template_name = 'staff_portal/content/form.html'
    success_url = reverse_lazy('staff_portal:content_list')

    def form_valid(self, form):
        messages.success(self.request, 'New text section added.')
        return super().form_valid(form)


# --- Team ---

class TeamListView(StaffRequiredMixin, ListView):
    model = TeamMember
    template_name = 'staff_portal/team/list.html'
    context_object_name = 'members'


class TeamCreateView(StaffRequiredMixin, CreateView):
    model = TeamMember
    form_class = TeamMemberForm
    template_name = 'staff_portal/team/form.html'
    success_url = reverse_lazy('staff_portal:team_list')

    def form_valid(self, form):
        messages.success(self.request, 'Team member added.')
        return super().form_valid(form)


class TeamUpdateView(StaffRequiredMixin, UpdateView):
    model = TeamMember
    form_class = TeamMemberForm
    template_name = 'staff_portal/team/form.html'
    success_url = reverse_lazy('staff_portal:team_list')

    def form_valid(self, form):
        messages.success(self.request, 'Team member updated.')
        return super().form_valid(form)


class TeamDeleteView(StaffRequiredMixin, DeleteView):
    model = TeamMember
    template_name = 'staff_portal/confirm_delete.html'
    success_url = reverse_lazy('staff_portal:team_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cancel_url'] = reverse('staff_portal:team_list')
        ctx['object_label'] = 'team member'
        return ctx


# --- Resources ---

class ResourceListView(StaffRequiredMixin, ListView):
    model = Resource
    template_name = 'staff_portal/resources/list.html'
    context_object_name = 'resources'
    paginate_by = 25

    def get_queryset(self):
        return Resource.objects.select_related('category').order_by('category__ordering', 'ordering')


class ResourceCreateView(StaffRequiredMixin, CreateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'staff_portal/resources/form.html'
    success_url = reverse_lazy('staff_portal:resource_list')

    def form_valid(self, form):
        messages.success(self.request, 'Resource added.')
        return super().form_valid(form)


class ResourceUpdateView(StaffRequiredMixin, UpdateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'staff_portal/resources/form.html'
    success_url = reverse_lazy('staff_portal:resource_list')

    def form_valid(self, form):
        messages.success(self.request, 'Resource updated.')
        return super().form_valid(form)


class ResourceDeleteView(StaffRequiredMixin, DeleteView):
    model = Resource
    template_name = 'staff_portal/confirm_delete.html'
    success_url = reverse_lazy('staff_portal:resource_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cancel_url'] = reverse('staff_portal:resource_list')
        ctx['object_label'] = 'resource'
        return ctx


# --- Settings ---

class DonationSettingsView(StaffRequiredMixin, UpdateView):
    model = DonationSettings
    form_class = DonationSettingsForm
    template_name = 'staff_portal/settings/donations.html'

    def get_object(self):
        return DonationSettings.load()

    def get_success_url(self):
        messages.success(self.request, 'Donation settings saved.')
        return reverse('staff_portal:donation_settings')


class HomepageSettingsView(StaffRequiredMixin, UpdateView):
    model = HomepageSettings
    form_class = HomepageSettingsForm
    template_name = 'staff_portal/settings/homepage.html'

    def get_object(self):
        return HomepageSettings.load()

    def get_success_url(self):
        messages.success(self.request, 'Homepage hero settings saved.')
        return reverse('staff_portal:homepage_settings')
