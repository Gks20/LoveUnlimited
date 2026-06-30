from django.core.management.base import BaseCommand

from frontend.po_compile import compile_locale


class Command(BaseCommand):
    help = 'Compile .po translation files to .mo (no GNU gettext required).'

    def handle(self, *args, **options):
        compile_locale('locale')
        self.stdout.write(self.style.SUCCESS('Compiled locale message files.'))
