from datetime import datetime

from frontend.models import DonationSettings, HomepageSettings


def site_globals(request):
    donation = DonationSettings.load()
    return {
        'current_year': datetime.now().year,
        'zeffy_form_link': donation.zeffy_form_link,
        'homepage_settings': HomepageSettings.load(),
    }
