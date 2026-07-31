from django.db import migrations

from staff_portal.content_registry import upsert_default_content


def seed_extended_ui_content(apps, schema_editor):
    upsert_default_content()


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0007_homepagesettings'),
    ]

    operations = [
        migrations.RunPython(seed_extended_ui_content, migrations.RunPython.noop),
    ]
