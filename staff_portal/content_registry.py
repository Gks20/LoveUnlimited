"""Registry of editable site content, preview pages, and default copy (EN/ES)."""

from django.utils import timezone

from calendar_app.models import Event
from frontend.models import DonationSettings, Resource, ResourceCategory, SiteContent, TeamMember

# Plain-text UI labels (single line, no HTML)
UI_TEXT_DEFAULTS = {
  'en': {
    'ui-nav-home': 'Home',
    'ui-nav-about': 'About',
    'ui-nav-events': 'Events',
    'ui-nav-resources': 'Resources',
    'ui-nav-contact': 'Contact',
    'ui-nav-donate': 'Donate',
    'ui-footer-quick-links': 'Quick Links',
    'ui-footer-about-us': 'About Us',
    'ui-footer-contact-info': 'Contact Info',
    'ui-footer-rights': 'All rights reserved.',
    'ui-footer-staff-login': 'Staff Login',
    'ui-home-donate-now': 'Donate Now',
    'ui-home-learn-more': 'Learn More',
    'ui-home-our-mission': 'Our Mission',
    'ui-home-how-we-help': 'How We Help',
    'ui-home-meals-title': 'Weekly Meal Service',
    'ui-home-housing-title': 'Housing & Essential Support',
    'ui-home-advocacy-title': 'Advocacy & Life Navigation',
    'ui-home-view-resources': 'View Resources',
    'ui-home-upcoming-events': 'Upcoming Events',
    'ui-home-view-all-events': 'View All Events',
    'ui-home-no-events': 'No events scheduled right now. Check back soon or contact us to stay in the loop.',
    'ui-home-view-calendar': 'View Events Calendar',
    'ui-home-cta-title': 'Make a Difference Today',
    'ui-home-volunteer': 'Volunteer',
    'ui-about-title': 'About Love Unlimited',
    'ui-about-mission-title': 'Our Mission',
    'ui-about-approach-title': 'Our Approach',
    'ui-about-values-title': 'Our Values',
    'ui-about-story-title': 'Our Story',
    'ui-about-impact-title': 'Our Impact',
    'ui-about-impact-serving': 'Serving Since',
    'ui-about-impact-meals': 'Meals Provided',
    'ui-about-impact-weekly': 'Saturday Service',
    'ui-about-impact-outreach': 'Outreach Model',
    'ui-about-team-title': 'Our Leadership Team',
    'ui-about-get-involved-title': 'Get Involved',
    'ui-about-btn-donate': 'Donate',
    'ui-about-btn-volunteer': 'Volunteer',
    'ui-about-btn-partner': 'Partner With Us',
    'ui-contact-title': 'Contact Us',
    'ui-contact-lead': (
        "We'd love to hear from you. Get in touch with us for questions, "
        "volunteer opportunities, or partnership inquiries."
    ),
    'ui-contact-label-address': 'Address',
    'ui-contact-label-phone': 'Phone',
    'ui-contact-label-email': 'Email',
    'ui-contact-label-hours': 'Hours',
    'ui-donate-title': 'Support Our Mission',
    'ui-donate-section-title': 'Make a Donation',
    'ui-donate-btn': 'Donate Now',
    'ui-donate-other-ways': 'Other Ways to Support Us',
    'ui-donate-tax-heading': 'Tax Deductible',
  },
  'es': {
    'ui-nav-home': 'Inicio',
    'ui-nav-about': 'Acerca',
    'ui-nav-events': 'Eventos',
    'ui-nav-resources': 'Recursos',
    'ui-nav-contact': 'Contacto',
    'ui-nav-donate': 'Donar',
    'ui-footer-quick-links': 'Enlaces Rápidos',
    'ui-footer-about-us': 'Acerca de Nosotros',
    'ui-footer-contact-info': 'Información de Contacto',
    'ui-footer-rights': 'Todos los derechos reservados.',
    'ui-footer-staff-login': 'Acceso del Personal',
    'ui-home-donate-now': 'Donar Ahora',
    'ui-home-learn-more': 'Conocer Más',
    'ui-home-our-mission': 'Nuestra Misión',
    'ui-home-how-we-help': 'Cómo Ayudamos',
    'ui-home-meals-title': 'Comidas Semanales',
    'ui-home-housing-title': 'Vivienda y Apoyo Esencial',
    'ui-home-advocacy-title': 'Defensa y Orientación',
    'ui-home-view-resources': 'Ver Recursos',
    'ui-home-upcoming-events': 'Próximos Eventos',
    'ui-home-view-all-events': 'Ver Todos los Eventos',
    'ui-home-no-events': (
        'No hay eventos programados por ahora. Vuelva pronto o contáctenos para mantenerse informado.'
    ),
    'ui-home-view-calendar': 'Ver Calendario de Eventos',
    'ui-home-cta-title': 'Marque la Diferencia Hoy',
    'ui-home-volunteer': 'Ser Voluntario',
    'ui-about-title': 'Acerca de Love Unlimited',
    'ui-about-mission-title': 'Nuestra Misión',
    'ui-about-approach-title': 'Nuestro Enfoque',
    'ui-about-values-title': 'Nuestros Valores',
    'ui-about-story-title': 'Nuestra Historia',
    'ui-about-impact-title': 'Nuestro Impacto',
    'ui-about-impact-serving': 'Sirviendo Desde',
    'ui-about-impact-meals': 'Comidas Proporcionadas',
    'ui-about-impact-weekly': 'Servicio del Sábado',
    'ui-about-impact-outreach': 'Modelo de Alcance',
    'ui-about-team-title': 'Nuestro Equipo de Liderazgo',
    'ui-about-get-involved-title': 'Participe',
    'ui-about-btn-donate': 'Donar',
    'ui-about-btn-volunteer': 'Ser Voluntario',
    'ui-about-btn-partner': 'Asóciese con Nosotros',
    'ui-contact-title': 'Contáctenos',
    'ui-contact-lead': (
        'Nos encantaría saber de usted. Comuníquese con nosotros para preguntas, '
        'oportunidades de voluntariado o consultas de asociación.'
    ),
    'ui-contact-label-address': 'Dirección',
    'ui-contact-label-phone': 'Teléfono',
    'ui-contact-label-email': 'Correo electrónico',
    'ui-contact-label-hours': 'Horario',
    'ui-donate-title': 'Apoye Nuestra Misión',
    'ui-donate-section-title': 'Hacer una Donación',
    'ui-donate-btn': 'Donar Ahora',
    'ui-donate-other-ways': 'Otras Formas de Apoyarnos',
    'ui-donate-tax-heading': 'Deducible de Impuestos',
  },
}

# HTML blocks added for visual editor / Spanish (body copy defaults stay in bootstrap_site)
UI_HTML_DEFAULTS = {
  'en': {
    'donate-zeffy-info': (
      'We partner with Zeffy for secure, transparent donation processing. This means 100% of '
      'your contribution goes directly to Love Unlimited—no fees, no deductions.'
    ),
    'donate-tax-body': (
      "Love Unlimited is a registered 501(c)(3) non-profit organization. Your generous donation "
      "is tax-deductible to the full extent allowed by law, and you'll receive a receipt for your records."
    ),
    'contact-preview-note': 'The contact form below is not editable here — visitors use it to send you messages.',
  },
  'es': {
    'donate-zeffy-info': (
      'Nos asociamos con Zeffy para un procesamiento de donaciones seguro y transparente. '
      'Esto significa que el 100% de su contribución va directamente a Love Unlimited, sin tarifas ni deducciones.'
    ),
    'donate-tax-body': (
      'Love Unlimited es una organización sin fines de lucro 501(c)(3) registrada. Su generosa donación '
      'es deducible de impuestos en la medida permitida por la ley, y recibirá un recibo para sus registros.'
    ),
    'contact-preview-note': (
      'El formulario de contacto a continuación no se puede editar aquí; los visitantes lo usan para enviarle mensajes.'
    ),
  },
}

PREVIEW_PAGES = {
    'home': {
        'label': 'Homepage',
        'template': 'frontend/home.html',
    },
    'about': {
        'label': 'About Us',
        'template': 'frontend/about.html',
    },
    'contact': {
        'label': 'Contact',
        'template': 'frontend/contact.html',
    },
    'donate': {
        'label': 'Donate',
        'template': 'frontend/donate.html',
    },
}

PLAIN_TEXT_KEYS = frozenset({
    'contact-email',
    *UI_TEXT_DEFAULTS['en'].keys(),
})

SINGLE_LINE_KEYS = PLAIN_TEXT_KEYS


def all_content_keys():
    from staff_portal.content_labels import CONTENT_SECTIONS

    keys = set()
    for _section_id, _title, _help, items in CONTENT_SECTIONS:
        for key, _label in items:
            keys.add(key)
    keys.update(UI_TEXT_DEFAULTS['en'].keys())
    keys.update(UI_HTML_DEFAULTS['en'].keys())
    return keys


def build_preview_context(page_id, request, *, edit_mode=False):
    """Build template context for a public page preview."""
    lang = request.GET.get('lang', 'en')
    if lang not in ('en', 'es'):
        lang = 'en'

    context = {
        'content_edit_mode': edit_mode,
        'preview_mode': edit_mode,
        'preview_lang': lang,
    }

    today = timezone.now().date()

    if page_id == 'home':
        context['upcoming_events'] = Event.objects.filter(
            date__gte=today,
            is_public=True,
        ).select_related('category').order_by('date')[:3]
    elif page_id == 'about':
        context['team_members'] = TeamMember.objects.filter(is_active=True)
    elif page_id == 'contact':
        from frontend.forms import ContactForm
        context['form'] = ContactForm()
    elif page_id == 'donate':
        context['donation_settings'] = DonationSettings.load()
    elif page_id == 'resources':
        categories = ResourceCategory.objects.all()
        resources_qs = Resource.objects.filter(is_active=True).select_related('category')
        grouped = {cat: [] for cat in categories}
        for resource in resources_qs:
            grouped[resource.category].append(resource)
        context.update({
            'query': '',
            'selected_category': None,
            'categories': categories,
            'grouped_resources': grouped,
            'total_results': resources_qs.count(),
        })

    return context, lang


def upsert_default_content():
    """Create missing SiteContent rows for UI defaults (used by migration/bootstrap)."""
    from frontend.management.commands.bootstrap_site import DEFAULT_CONTENT, SPANISH_CONTENT

    created = 0
    all_defaults = {}
    for key, body in DEFAULT_CONTENT.items():
        all_defaults.setdefault(key, {})['en'] = body
    for key, body in SPANISH_CONTENT.items():
        all_defaults.setdefault(key, {})['es'] = body
    for key, body in UI_TEXT_DEFAULTS['en'].items():
        all_defaults.setdefault(key, {})['en'] = body
    for key, body in UI_TEXT_DEFAULTS['es'].items():
        all_defaults.setdefault(key, {})['es'] = body
    for key, body in UI_HTML_DEFAULTS['en'].items():
        all_defaults.setdefault(key, {})['en'] = body
    for key, body in UI_HTML_DEFAULTS['es'].items():
        all_defaults.setdefault(key, {})['es'] = body

    for key, translations in all_defaults.items():
        for language, body in translations.items():
            _, was_created = SiteContent.objects.get_or_create(
                key=key,
                language=language,
                defaults={
                    'title': key.replace('-', ' ').title(),
                    'body': body,
                },
            )
            if was_created:
                created += 1
    return created
