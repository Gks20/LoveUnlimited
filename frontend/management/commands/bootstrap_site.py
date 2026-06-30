from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import time, timedelta

from calendar_app.models import Event, EventCategory
from frontend.models import SiteContent, DonationSettings, TeamMember, Resource, ResourceCategory
from frontend.resource_seed import DEFAULT_RESOURCE_CATEGORIES, DEFAULT_RESOURCES

DEFAULT_CONTENT = {
    'home-hero': (
        "We're a passionate grassroots organization dedicated to serving our community's most vulnerable members. "
        "Through generous community donations and volunteer support, we provide essential meals, resources, and hope "
        "to those experiencing homelessness and hardship."
    ),
    'home-mission': (
        "We exist to be a beacon of hope in our community. Love Unlimited combines grassroots passion with practical "
        "action, providing nutritious meals and comprehensive support services to individuals and families facing "
        "homelessness and economic hardship. Every interaction is guided by our belief that everyone deserves dignity, "
        "respect, and a path forward."
    ),
    'home-service-meals': (
        "Every Saturday, we serve nutritious meals with love and dignity. These weekly gatherings are more than just "
        "food distribution—they're opportunities to build relationships, establish trust, and create a welcoming "
        "community. Since 2020, we've served over 4,000 meals with care and compassion."
    ),
    'home-service-housing': (
        "We connect individuals with emergency housing resources and provide essential supplies when permanent housing "
        "is secured. From basic hygiene items to household necessities, we ensure that fundamental needs are met "
        "during critical transition periods."
    ),
    'home-service-advocacy': (
        "We serve as trusted advocates, helping navigate complex benefit systems, connecting individuals with treatment "
        "resources, and providing essential clothing and hygiene supplies. Our goal is to remove barriers and create "
        "pathways to stability and recovery."
    ),
    'home-cta': (
        "Your support helps us continue our mission of serving those in need with love and compassion."
    ),
    'about-intro': (
        "We're a dedicated team of volunteers and community members united by a shared commitment to serving those in need. "
        "Through collaboration, compassion, and unwavering support, we work together to ensure every person we serve "
        "receives the dignity and care they deserve."
    ),
    'about-mission': (
        "We are a community-driven organization committed to addressing homelessness and poverty through direct service, "
        "compassionate support, and sustainable solutions. Powered by local donations and volunteer dedication, we create "
        "meaningful connections that transform lives."
    ),
    'about-approach': (
        "While our Saturday meals are the foundation of our work, they represent so much more than food service. These "
        "weekly gatherings are our primary way of building meaningful relationships, establishing trust, and creating "
        "a supportive community where everyone feels valued and heard."
    ),
    'about-values': (
        '<p><strong>Human Dignity:</strong> Every person we serve deserves our best efforts, genuine care, '
        'and respectful guidance.</p>'
        '<p><strong>Compassionate Service:</strong> Kindness and respect are at the heart of every interaction.</p>'
        '<p><strong>Community Support:</strong> We provide a stable support network for those who may lack '
        'one during difficult times.</p>'
        '<p><strong>Holistic Care:</strong> We address both immediate needs and long-term goals for lasting positive change.</p>'
    ),
    'about-story-1': (
        "Love Unlimited began as a mobile outreach initiative in 2020, driven by a simple yet powerful mission: to serve "
        "our community's most vulnerable members with dignity and compassion. As a registered non-profit organization "
        "based in Indiana, we've grown from humble beginnings into a trusted community resource."
    ),
    'about-story-2': (
        "Since our founding, we've proudly provided over <strong>4,000 meals</strong> to individuals "
        "and families in need. Beyond nourishment, we offer essential clothing and hygiene supplies for men, women, and "
        "children of all ages. Every interaction is rooted in our core values of "
        "<strong>love</strong>, <strong>respect</strong>, and <strong>kindness</strong>—qualities we believe everyone "
        "deserves, regardless of their circumstances."
    ),
    'about-story-3': (
        "Our impact extends far beyond our Saturday meal services. Once trust is established, Love Unlimited becomes a "
        "comprehensive support system, offering advocacy for government benefits, connecting individuals to emergency "
        "housing resources, providing essential supplies for those transitioning to stable housing, and facilitating "
        "pathways to treatment centers when needed. We're here for the long journey, not just the immediate need."
    ),
    'about-get-involved': (
        'There are many ways to support our mission and help make a difference in our community.'
    ),
    'donate-intro': (
        "Your generous support enables us to continue providing essential services to our community's most vulnerable "
        "members. Every donation, regardless of size, creates meaningful change in someone's life and strengthens our "
        "collective impact."
    ),
    'footer-tagline': (
        'A grassroots force providing meals and support to local homeless and less fortunate.'
    ),
    'contact-email': 'loveunlimitedcommunityoutreach@gmail.com',
    'contact-phone': '(502) 509-7563',
    'contact-address': 'Central Christian Church<br>1315 E. Spring Street<br>New Albany, IN 47150',
    'contact-hours': 'Monday - Friday: 9:00 AM - 5:00 PM<br>Saturday: 10:00 AM - 2:00 PM<br>Sunday: Closed',
}

SPANISH_CONTENT = {
    'home-hero': (
        'Somos una organización comunitaria dedicada a servir a los miembros más vulnerables de nuestra comunidad. '
        'Gracias a donaciones generosas y voluntarios, ofrecemos comidas esenciales, recursos y esperanza '
        'a quienes enfrentan la falta de vivienda y dificultades económicas.'
    ),
    'home-mission': (
        'Existimos para ser un faro de esperanza en nuestra comunidad. Love Unlimited combina pasión comunitaria '
        'con acción práctica, brindando comidas nutritivas y apoyo integral a personas y familias en situación '
        'de calle o dificultades económicas.'
    ),
    'home-service-meals': (
        'Cada sábado servimos comidas nutritivas con amor y dignidad. Estas reuniones semanales son más que '
        'distribución de alimentos: son oportunidades para construir relaciones y crear una comunidad acogedora.'
    ),
    'home-service-housing': (
        'Conectamos a las personas con recursos de vivienda de emergencia y proveemos artículos esenciales '
        'cuando se consigue vivienda permanente.'
    ),
    'home-service-advocacy': (
        'Somos defensores de confianza, ayudando a navegar sistemas de beneficios y conectando a las personas '
        'con recursos de tratamiento y artículos de higiene esenciales.'
    ),
    'home-cta': 'Su apoyo nos ayuda a continuar nuestra misión de servir a quienes más lo necesitan.',
    'about-intro': (
        'Somos un equipo dedicado de voluntarios y miembros de la comunidad unidos por el compromiso '
        'de servir a quienes lo necesitan.'
    ),
    'about-mission': (
        'Somos una organización impulsada por la comunidad, comprometida con abordar la falta de vivienda '
        'y la pobreza mediante servicio directo y apoyo compasivo.'
    ),
    'about-approach': (
        'Nuestras comidas del sábado son la base de nuestro trabajo y una forma de construir relaciones '
        'significativas y crear una comunidad de apoyo.'
    ),
    'about-values': (
        '<p><strong>Dignidad humana:</strong> Cada persona merece nuestro mejor esfuerzo y respeto.</p>'
        '<p><strong>Servicio compasivo:</strong> La amabilidad está en el corazón de cada interacción.</p>'
        '<p><strong>Apoyo comunitario:</strong> Ofrecemos una red estable para quienes la necesitan.</p>'
        '<p><strong>Cuidado integral:</strong> Atendemos necesidades inmediatas y metas a largo plazo.</p>'
    ),
    'about-story-1': (
        'Love Unlimited comenzó como una iniciativa móvil en 2020, impulsada por una misión simple: '
        'servir con dignidad y compasión a los miembros más vulnerables de nuestra comunidad.'
    ),
    'about-story-2': (
        'Desde nuestra fundación, hemos proporcionado más de <strong>4,000 comidas</strong> a personas '
        'y familias necesitadas, además de ropa e higiene esenciales.'
    ),
    'about-story-3': (
        'Nuestro impacto va más allá de las comidas del sábado: ofrecemos defensa, vivienda de emergencia '
        'y conexiones con centros de tratamiento cuando se necesitan.'
    ),
    'about-get-involved': 'Hay muchas formas de apoyar nuestra misión y marcar la diferencia.',
    'donate-intro': (
        'Su generoso apoyo nos permite continuar brindando servicios esenciales a los miembros más '
        'vulnerables de nuestra comunidad.'
    ),
    'footer-tagline': 'Una fuerza comunitaria que ofrece comidas y apoyo a personas sin hogar y en necesidad.',
    'contact-email': 'loveunlimitedcommunityoutreach@gmail.com',
    'contact-phone': '(502) 509-7563',
    'contact-address': 'Central Christian Church<br>1315 E. Spring Street<br>New Albany, IN 47150',
    'contact-hours': 'Lunes - Viernes: 9:00 AM - 5:00 PM<br>Sábado: 10:00 AM - 2:00 PM<br>Domingo: Cerrado',
}

DEFAULT_TEAM = [
    {
        'name': 'Stephanie Woodward',
        'role': 'Executive Director, President',
        'bio': "Leading Love Unlimited with passion and dedication to serve our community's most vulnerable members.",
        'ordering': 1,
    },
    {
        'name': 'Chris Kahafer',
        'role': 'Vice President',
        'bio': 'Supporting our mission and helping guide the strategic direction of Love Unlimited.',
        'ordering': 2,
    },
    {
        'name': 'Cathy Higgins',
        'role': 'Program Director, Treasurer',
        'bio': 'Managing our programs and financial operations to ensure effective service delivery.',
        'ordering': 3,
    },
]


class Command(BaseCommand):
    help = 'Seed default site content, team members, and donation settings.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--demo-events',
            action='store_true',
            help='Create sample public events for local development only.',
        )

    def handle(self, *args, **options):
        DonationSettings.load()
        self.stdout.write(self.style.SUCCESS('Donation settings ready.'))

        created = 0
        for key, body in DEFAULT_CONTENT.items():
            for lang in ('en', 'es'):
                lang_body = SPANISH_CONTENT.get(key, body) if lang == 'es' else body
                _, was_created = SiteContent.objects.get_or_create(
                    key=key,
                    language=lang,
                    defaults={'title': key.replace('-', ' ').title(), 'body': lang_body},
                )
                if was_created:
                    created += 1
        self.stdout.write(self.style.SUCCESS(f'Site content: {created} new blocks (en + es).'))

        resource_cats = {}
        cat_created = 0
        for cat_data in DEFAULT_RESOURCE_CATEGORIES:
            cat, was_created = ResourceCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'icon_class': cat_data['icon_class'],
                    'ordering': cat_data['ordering'],
                },
            )
            resource_cats[cat_data['slug']] = cat
            if was_created:
                cat_created += 1
        resource_created = 0
        for item in DEFAULT_RESOURCES:
            cat = resource_cats[item['category']]
            _, was_created = Resource.objects.get_or_create(
                category=cat,
                name=item['name'],
                defaults={
                    'description': item.get('description', ''),
                    'address': item.get('address', ''),
                    'phone': item.get('phone', ''),
                    'website': item.get('website', ''),
                    'hours': item.get('hours', ''),
                    'tags': item.get('tags', ''),
                    'ordering': item.get('ordering', 0),
                    'is_active': True,
                },
            )
            if was_created:
                resource_created += 1
        self.stdout.write(self.style.SUCCESS(
            f'Resources: {cat_created} categories, {resource_created} listings created.'
        ))

        team_created = 0
        for member in DEFAULT_TEAM:
            _, was_created = TeamMember.objects.get_or_create(
                name=member['name'],
                defaults=member,
            )
            if was_created:
                team_created += 1
        self.stdout.write(self.style.SUCCESS(f'Team members: {team_created} created.'))

        if options['demo_events']:
            category, _ = EventCategory.objects.get_or_create(
                name='Community',
                defaults={'color': '#007bff', 'description': 'Community events'},
            )
            event_date = timezone.now().date() + timedelta(days=14)
            Event.objects.get_or_create(
                title='Saturday Meal Service',
                date=event_date,
                defaults={
                    'description': 'Weekly community meal service.',
                    'category': category,
                    'start_time': time(11, 0),
                    'end_time': time(14, 0),
                    'location': 'Community Center',
                    'is_public': True,
                    'max_attendees': 50,
                },
            )
            self.stdout.write(self.style.SUCCESS('Demo event created.'))
