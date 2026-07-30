from django.db import migrations


CONTACT_UPDATES = {
    'contact-address': {
        'en': (
            'Love Unlimited c/o<br>Central Christian Church<br>'
            '1315 E. Spring Street<br>New Albany, IN 47150'
        ),
        'es': (
            'Love Unlimited c/o<br>Central Christian Church<br>'
            '1315 E. Spring Street<br>New Albany, IN 47150'
        ),
    },
    'contact-contacts': {
        'en': (
            'Stephanie Woodward - <a href="tel:+18123992954">(812) 399-2954</a><br>'
            'Cathy Higgins - <a href="tel:+15025580642">(502) 558-0642</a>'
        ),
        'es': (
            'Stephanie Woodward - <a href="tel:+18123992954">(812) 399-2954</a><br>'
            'Cathy Higgins - <a href="tel:+15025580642">(502) 558-0642</a>'
        ),
    },
    'contact-hours': {
        'en': 'Monday - Friday: 9:00 AM - 5:00 PM<br>Saturday: 1:00 PM - 3:00 PM<br>Sunday: Closed',
        'es': 'Lunes - Viernes: 9:00 AM - 5:00 PM<br>Sábado: 1:00 PM - 3:00 PM<br>Domingo: Cerrado',
    },
}


def update_contact_content(apps, schema_editor):
    SiteContent = apps.get_model('frontend', 'SiteContent')

    for key, translations in CONTACT_UPDATES.items():
        for language, body in translations.items():
            SiteContent.objects.update_or_create(
                key=key,
                language=language,
                defaults={
                    'title': key.replace('-', ' ').title(),
                    'body': body,
                },
            )


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0004_teammember'),
    ]

    operations = [
        migrations.RunPython(update_contact_content, migrations.RunPython.noop),
    ]
