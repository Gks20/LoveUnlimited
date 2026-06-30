from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.text import slugify
from django.views.decorators.http import require_GET, require_POST

from .forms import EventRegistrationForm
from .models import Event, EventRegistration

REGISTRATION_MODAL_SESSION_KEY = 'event_registration_modal'


@require_POST
def register_for_event(request, pk):
    event = get_object_or_404(Event, pk=pk, is_public=True)

    if not event.is_upcoming:
        messages.error(request, 'This event has already passed.')
        return redirect('frontend:calendar')

    if event.max_attendees is not None:
        if event.eventregistration_set.count() >= event.max_attendees:
            messages.error(request, 'This event is full.')
            return redirect('frontend:calendar')

    form = EventRegistrationForm(request.POST)
    if not form.is_valid():
        request.session[REGISTRATION_MODAL_SESSION_KEY] = {
            'event_id': pk,
            'errors': form.errors.get_json_data(),
            'data': {
                field: request.POST.get(field, '')
                for field in form.fields
            },
        }
        messages.error(request, 'Please correct the errors below and try again.')
        return redirect('frontend:calendar')

    email = form.cleaned_data['email']
    if EventRegistration.objects.filter(event=event, email=email).exists():
        messages.error(request, 'You are already registered for this event with that email.')
        return redirect('frontend:calendar')

    registration = form.save(commit=False)
    registration.event = event
    try:
        registration.save()
    except IntegrityError:
        messages.error(request, 'You are already registered for this event with that email.')
        return redirect('frontend:calendar')

    messages.success(request, f'You are registered for {event.title}.')
    return redirect('frontend:calendar')


@require_GET
def event_ics(request, pk):
    event = get_object_or_404(Event, pk=pk, is_public=True)
    start = f'{event.date.strftime("%Y%m%d")}T{event.start_time.strftime("%H%M%S")}'
    end = f'{event.date.strftime("%Y%m%d")}T{event.end_time.strftime("%H%M%S")}'
    location = event.location.replace(',', '\\,') if event.location else ''
    description = (event.description or '').replace('\n', '\\n').replace(',', '\\,')

    ics = (
        'BEGIN:VCALENDAR\r\n'
        'VERSION:2.0\r\n'
        'PRODID:-//Love Unlimited//EN\r\n'
        'BEGIN:VEVENT\r\n'
        f'UID:event-{event.pk}@loveunlimited\r\n'
        f'DTSTAMP:{event.created_at.strftime("%Y%m%dT%H%M%SZ")}\r\n'
        f'DTSTART:{start}\r\n'
        f'DTEND:{end}\r\n'
        f'SUMMARY:{event.title}\r\n'
        f'DESCRIPTION:{description}\r\n'
        f'LOCATION:{location}\r\n'
        'END:VEVENT\r\n'
        'END:VCALENDAR\r\n'
    )
    response = HttpResponse(ics, content_type='text/calendar; charset=utf-8')
    filename = slugify(event.title) or 'event'
    response['Content-Disposition'] = f'attachment; filename="{filename}.ics"'
    return response
