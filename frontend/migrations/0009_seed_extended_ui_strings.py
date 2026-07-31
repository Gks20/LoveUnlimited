from django.db import migrations

from staff_portal.content_registry import upsert_default_content


def seed_extended_ui_strings(apps, schema_editor):
    upsert_default_content()


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0008_seed_extended_ui_content'),
    ]

    operations = [
        migrations.RunPython(seed_extended_ui_strings, migrations.RunPython.noop),
    ]
