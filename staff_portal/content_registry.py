"""Registry of editable site content, preview pages, and default copy (EN/ES)."""

from django.utils import timezone

from calendar_app.models import Event
from frontend.models import DonationSettings, HomepageSettings, Resource, ResourceCategory, SiteContent, TeamMember

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
    'ui-home-brand': 'Love Unlimited',
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
    'ui-calendar-title': 'Events & Calendar',
    'ui-calendar-lead': 'Join us for upcoming events, volunteer opportunities, and community gatherings. Everyone is welcome!',
    'ui-calendar-upcoming': 'Upcoming Events',
    'ui-calendar-past': 'Past Events',
    'ui-calendar-empty-title': 'No Upcoming Events',
    'ui-calendar-empty-lead': 'Check back soon for upcoming events and volunteer opportunities!',
    'ui-calendar-contact-updates': 'Contact Us for Updates',
    'ui-calendar-stay-updated': 'Stay Updated',
    'ui-calendar-stay-lead': 'Contact us to hear about upcoming events, volunteer opportunities, and community news.',
    'ui-contact-form-title': 'Send Us a Message',
    'ui-contact-send-message': 'Send Message',
    'ui-contact-volunteer-title': 'Volunteer With Us',
    'ui-contact-volunteer-lead': 'Join our amazing team of volunteers and make a direct impact in your community. We have opportunities for individuals, families, and groups.',
    'ui-resources-title': 'Community Resources',
    'ui-resources-lead': 'Search and filter verified local assistance programs. Data is maintained by our team.',
    'ui-form-first-name': 'First Name',
    'ui-form-last-name': 'Last Name',
    'ui-form-email': 'Email Address',
    'ui-form-phone': 'Phone Number',
    'ui-form-subject': 'Subject',
    'ui-form-message': 'Message',
    'ui-form-subject-volunteer': 'Volunteer Opportunities',
    'ui-form-subject-donate': 'Donation Questions',
    'ui-form-subject-services': 'Services Information',
    'ui-form-subject-partnership': 'Partnership Inquiry',
    'ui-form-subject-media': 'Media Inquiry',
    'ui-form-subject-other': 'Other',
    'ui-form-message-min': 'Message must be at least 10 characters for sufficient detail.',
    'ui-contact-info-heading': 'Contact Information',
    'ui-contact-volunteer-food-title': 'Food Service',
    'ui-contact-volunteer-food-desc': 'Help prepare and serve meals to community members in need.',
    'ui-contact-volunteer-donate-title': 'Donation Sorting',
    'ui-contact-volunteer-donate-desc': 'Organize, sort, and distribute donated items to the community.',
    'ui-contact-volunteer-event-title': 'Event Support',
    'ui-contact-volunteer-event-desc': 'Help with community events, fundraisers, and special programs.',
    'ui-contact-volunteer-cta': 'Ready to get started? Use the contact form above and choose Volunteer in the subject line, or call us directly.',
    'ui-contact-volunteer-note': 'All volunteers complete a brief orientation and background check.',
    'ui-donate-volunteer-body': 'Join our passionate team of volunteers and make a direct, hands-on impact in your community.',
    'ui-donate-items-title': 'Donate Items',
    'ui-donate-items-body': 'We gratefully accept non-perishable food, gently used clothing, and essential hygiene items.',
    'ui-event-register': 'Register',
    'ui-event-full': 'Event Full',
    'ui-event-past': 'Past Event',
    'ui-event-add-calendar': 'Add to Calendar',
    'ui-event-contact': 'Contact',
    'ui-event-registered': 'registered',
    'ui-reg-modal-title': 'Event Registration',
    'ui-reg-first-name': 'First Name',
    'ui-reg-last-name': 'Last Name',
    'ui-reg-email': 'Email Address',
    'ui-reg-phone': 'Phone Number',
    'ui-reg-notes': 'Special Notes/Requirements',
    'ui-reg-cancel': 'Cancel',
    'ui-reg-submit': 'Register',
    'ui-modal-close': 'Close',
    'ui-about-impact-weekly-value': 'Weekly',
    'ui-about-impact-mobile-value': 'Mobile',
    'ui-resources-helplines-label': 'Emergency and quick help numbers',
    'ui-resources-emergency': 'Emergency',
    'ui-resources-crisis-lifeline': 'Crisis Lifeline',
    'ui-resources-suicide-crisis': 'Suicide & Crisis',
    'ui-resources-domestic-violence': 'Domestic Violence',
    'ui-resources-call-211': 'Call 211',
    'ui-resources-211-desc': '24/7 resource helpline',
    'ui-resources-white-flag': 'White Flag Shelter',
    'ui-resources-saturday-meals': 'Saturday meals',
    'ui-resources-crisis-support': 'Crisis Support',
    'ui-resources-call-text-988': 'Call or text 988',
    'ui-resources-search-label': 'Search resources',
    'ui-resources-search-placeholder': 'Search by name, service, or keyword…',
    'ui-resources-category-label': 'Category',
    'ui-resources-all-categories': 'All Categories',
    'ui-resources-search-btn': 'Search',
    'ui-resources-clear-btn': 'Clear',
    'ui-resources-one-result': '1 resource found',
    'ui-resources-many-results': 'resources found',
    'ui-resources-jump-category': 'Jump to category',
    'ui-resources-no-match': 'No resources match your search. Try different keywords or',
    'ui-resources-view-all': 'view all resources',
    'ui-resources-listings-label': 'Resource listings',
    'ui-resources-visit-website': 'Visit website',
    'ui-resources-none-in-category': 'No resources in this category',
    'ui-resources-matching': 'matching',
    'ui-resources-check-back': 'Check back later or call 211 for assistance.',
    'ui-resources-coming-soon': 'Resources Coming Soon',
    'ui-resources-building': 'Our team is building this directory. Call 211 for immediate assistance.',
    'ui-resources-before-you-go': 'Before You Go',
    'ui-resources-tip-call-title': 'Call first',
    'ui-resources-tip-call-desc': 'Verify hours, availability, and requirements.',
    'ui-resources-tip-id-title': 'Bring ID',
    'ui-resources-tip-id-desc': 'Photo ID and proof of address are often required.',
    'ui-resources-tip-paperwork-title': 'Bring paperwork',
    'ui-resources-tip-paperwork-desc': 'Income statements, bills, and related documents.',
    'ui-resources-tip-plan-title': 'Plan ahead',
    'ui-resources-tip-plan-desc': 'Some services have waiting lists or need appointments.',
    'ui-resources-help-heading': 'Need help finding the right resource?',
    'ui-resources-help-lead': 'Our staff can help connect you with services for your situation.',
    'ui-resources-disclaimer': 'Information is for general reference only. Services and hours may change — please call ahead to verify. Love Unlimited is not responsible for services provided by other organizations.',
    'ui-resources-updated': 'Updated',
    'ui-resources-back-to-top': 'Back to top',
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
    'ui-home-brand': 'Love Unlimited',
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
    'ui-calendar-title': 'Eventos y Calendario',
    'ui-calendar-lead': 'Únase a nuestros eventos, oportunidades de voluntariado y reuniones comunitarias. ¡Todos son bienvenidos!',
    'ui-calendar-upcoming': 'Próximos Eventos',
    'ui-calendar-past': 'Eventos Pasados',
    'ui-calendar-empty-title': 'No Hay Próximos Eventos',
    'ui-calendar-empty-lead': '¡Vuelva pronto para ver eventos y oportunidades de voluntariado!',
    'ui-calendar-contact-updates': 'Contáctenos para Actualizaciones',
    'ui-calendar-stay-updated': 'Manténgase Informado',
    'ui-calendar-stay-lead': 'Contáctenos para conocer eventos, oportunidades de voluntariado y noticias comunitarias.',
    'ui-contact-form-title': 'Envíenos un Mensaje',
    'ui-contact-send-message': 'Enviar Mensaje',
    'ui-contact-volunteer-title': 'Sea Voluntario con Nosotros',
    'ui-contact-volunteer-lead': 'Únase a nuestro equipo de voluntarios y marque la diferencia en su comunidad. Hay oportunidades para personas, familias y grupos.',
    'ui-resources-title': 'Recursos Comunitarios',
    'ui-resources-lead': 'Busque y filtre programas locales de asistencia verificados. Nuestro equipo mantiene esta información.',
    'ui-form-first-name': 'Nombre',
    'ui-form-last-name': 'Apellido',
    'ui-form-email': 'Correo electrónico',
    'ui-form-phone': 'Número de teléfono',
    'ui-form-subject': 'Asunto',
    'ui-form-message': 'Mensaje',
    'ui-form-subject-volunteer': 'Oportunidades de voluntariado',
    'ui-form-subject-donate': 'Preguntas sobre donaciones',
    'ui-form-subject-services': 'Información sobre servicios',
    'ui-form-subject-partnership': 'Consulta de asociación',
    'ui-form-subject-media': 'Consulta de medios',
    'ui-form-subject-other': 'Otro',
    'ui-form-message-min': 'El mensaje debe tener al menos 10 caracteres con suficiente detalle.',
    'ui-contact-info-heading': 'Información de contacto',
    'ui-contact-volunteer-food-title': 'Servicio de comidas',
    'ui-contact-volunteer-food-desc': 'Ayude a preparar y servir comidas a miembros de la comunidad.',
    'ui-contact-volunteer-donate-title': 'Clasificación de donaciones',
    'ui-contact-volunteer-donate-desc': 'Organice, clasifique y distribuya artículos donados a la comunidad.',
    'ui-contact-volunteer-event-title': 'Apoyo en eventos',
    'ui-contact-volunteer-event-desc': 'Ayude con eventos comunitarios, recaudaciones y programas especiales.',
    'ui-contact-volunteer-cta': '¿Listo para comenzar? Use el formulario de contacto arriba y elija Voluntariado en el asunto, o llámenos directamente.',
    'ui-contact-volunteer-note': 'Todos los voluntarios completan una breve orientación y verificación de antecedentes.',
    'ui-donate-volunteer-body': 'Únase a nuestro equipo de voluntarios y marque la diferencia directamente en su comunidad.',
    'ui-donate-items-title': 'Donar artículos',
    'ui-donate-items-body': 'Aceptamos con gratitud alimentos no perecederos, ropa usada en buen estado y artículos de higiene esenciales.',
    'ui-event-register': 'Registrarse',
    'ui-event-full': 'Evento lleno',
    'ui-event-past': 'Evento pasado',
    'ui-event-add-calendar': 'Agregar al calendario',
    'ui-event-contact': 'Contacto',
    'ui-event-registered': 'registrados',
    'ui-reg-modal-title': 'Registro de evento',
    'ui-reg-first-name': 'Nombre',
    'ui-reg-last-name': 'Apellido',
    'ui-reg-email': 'Correo electrónico',
    'ui-reg-phone': 'Número de teléfono',
    'ui-reg-notes': 'Notas o requisitos especiales',
    'ui-reg-cancel': 'Cancelar',
    'ui-reg-submit': 'Registrarse',
    'ui-modal-close': 'Cerrar',
    'ui-about-impact-weekly-value': 'Semanal',
    'ui-about-impact-mobile-value': 'Móvil',
    'ui-resources-helplines-label': 'Números de emergencia y ayuda rápida',
    'ui-resources-emergency': 'Emergencia',
    'ui-resources-crisis-lifeline': 'Línea de crisis',
    'ui-resources-suicide-crisis': 'Suicidio y crisis',
    'ui-resources-domestic-violence': 'Violencia doméstica',
    'ui-resources-call-211': 'Llame al 211',
    'ui-resources-211-desc': 'Línea de recursos 24/7',
    'ui-resources-white-flag': 'Refugio White Flag',
    'ui-resources-saturday-meals': 'Comidas del sábado',
    'ui-resources-crisis-support': 'Apoyo en crisis',
    'ui-resources-call-text-988': 'Llame o envíe mensaje al 988',
    'ui-resources-search-label': 'Buscar recursos',
    'ui-resources-search-placeholder': 'Buscar por nombre, servicio o palabra clave…',
    'ui-resources-category-label': 'Categoría',
    'ui-resources-all-categories': 'Todas las categorías',
    'ui-resources-search-btn': 'Buscar',
    'ui-resources-clear-btn': 'Borrar',
    'ui-resources-one-result': '1 recurso encontrado',
    'ui-resources-many-results': 'recursos encontrados',
    'ui-resources-jump-category': 'Ir a categoría',
    'ui-resources-no-match': 'Ningún recurso coincide con su búsqueda. Pruebe otras palabras clave o',
    'ui-resources-view-all': 'ver todos los recursos',
    'ui-resources-listings-label': 'Listado de recursos',
    'ui-resources-visit-website': 'Visitar sitio web',
    'ui-resources-none-in-category': 'No hay recursos en esta categoría',
    'ui-resources-matching': 'que coinciden con',
    'ui-resources-check-back': 'Vuelva más tarde o llame al 211 para asistencia.',
    'ui-resources-coming-soon': 'Recursos próximamente',
    'ui-resources-building': 'Nuestro equipo está creando este directorio. Llame al 211 para asistencia inmediata.',
    'ui-resources-before-you-go': 'Antes de ir',
    'ui-resources-tip-call-title': 'Llame primero',
    'ui-resources-tip-call-desc': 'Verifique horarios, disponibilidad y requisitos.',
    'ui-resources-tip-id-title': 'Traiga identificación',
    'ui-resources-tip-id-desc': 'A menudo se requiere identificación con foto y comprobante de domicilio.',
    'ui-resources-tip-paperwork-title': 'Traiga documentos',
    'ui-resources-tip-paperwork-desc': 'Estados de ingresos, facturas y documentos relacionados.',
    'ui-resources-tip-plan-title': 'Planifique con anticipación',
    'ui-resources-tip-plan-desc': 'Algunos servicios tienen listas de espera o requieren citas.',
    'ui-resources-help-heading': '¿Necesita ayuda para encontrar el recurso adecuado?',
    'ui-resources-help-lead': 'Nuestro personal puede ayudarle a conectarse con servicios para su situación.',
    'ui-resources-disclaimer': 'La información es solo de referencia general. Los servicios y horarios pueden cambiar — llame con anticipación para verificar. Love Unlimited no es responsable de los servicios proporcionados por otras organizaciones.',
    'ui-resources-updated': 'Actualizado',
    'ui-resources-back-to-top': 'Volver arriba',
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
    'calendar': {
        'label': 'Events',
        'template': 'frontend/calendar.html',
    },
    'resources': {
        'label': 'Resources',
        'template': 'frontend/resources.html',
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
    elif page_id == 'calendar':
        today = timezone.now().date()
        base_qs = Event.objects.filter(is_public=True).select_related('category')
        context['upcoming_events'] = base_qs.filter(date__gte=today).order_by('date', 'start_time')
        context['past_events'] = base_qs.filter(date__lt=today).order_by('-date', '-start_time')
        context['registration_modal'] = None
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
