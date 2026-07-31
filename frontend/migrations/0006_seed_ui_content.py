from django.db import migrations

from staff_portal.content_registry import upsert_default_content


def seed_ui_content(apps, schema_editor):
    upsert_default_content()


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_update_contact_content'),
    ]

    operations = [
        migrations.RunPython(seed_ui_content, migrations.RunPython.noop),
    ]
