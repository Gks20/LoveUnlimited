"""Plain-language names for site content blocks — shown instead of technical keys."""

CONTENT_SECTIONS = [
    (
        'home',
        'Homepage',
        'Text visitors see on the main page of your website.',
        [
            ('home-hero', 'Welcome message (top of page)'),
            ('home-mission', 'Our mission section'),
            ('home-service-meals', 'Meals service description'),
            ('home-service-housing', 'Housing help description'),
            ('home-service-advocacy', 'Advocacy service description'),
            ('home-cta', 'Call-to-action at the bottom'),
            ('ui-home-donate-now', 'Donate Now button'),
            ('ui-home-learn-more', 'Learn More button'),
            ('ui-home-our-mission', 'Our Mission heading'),
            ('ui-home-how-we-help', 'How We Help heading'),
            ('ui-home-meals-title', 'Meals service card title'),
            ('ui-home-housing-title', 'Housing card title'),
            ('ui-home-advocacy-title', 'Advocacy card title'),
            ('ui-home-view-resources', 'View Resources link'),
            ('ui-home-upcoming-events', 'Upcoming Events heading'),
            ('ui-home-view-all-events', 'View All Events button'),
            ('ui-home-no-events', 'No events message'),
            ('ui-home-view-calendar', 'View Events Calendar button'),
            ('ui-home-cta-title', 'Bottom call-to-action heading'),
            ('ui-home-volunteer', 'Volunteer button'),
        ],
    ),
    (
        'about',
        'About Us page',
        'Text on the About Us page.',
        [
            ('about-intro', 'Introduction'),
            ('about-mission', 'Mission statement'),
            ('about-approach', 'Our approach'),
            ('about-values', 'Our values'),
            ('about-story-1', 'Our story (part 1)'),
            ('about-story-2', 'Our story (part 2)'),
            ('about-story-3', 'Our story (part 3)'),
            ('about-get-involved', 'Get involved section'),
            ('ui-about-title', 'Page title'),
            ('ui-about-mission-title', 'Mission card title'),
            ('ui-about-approach-title', 'Approach card title'),
            ('ui-about-values-title', 'Values card title'),
            ('ui-about-story-title', 'Our Story heading'),
            ('ui-about-impact-title', 'Our Impact heading'),
            ('ui-about-impact-serving', 'Serving Since label'),
            ('ui-about-impact-meals', 'Meals Provided label'),
            ('ui-about-impact-weekly', 'Saturday Service label'),
            ('ui-about-impact-outreach', 'Outreach Model label'),
            ('ui-about-team-title', 'Leadership team heading'),
            ('ui-about-get-involved-title', 'Get Involved heading'),
            ('ui-about-btn-donate', 'Donate button'),
            ('ui-about-btn-volunteer', 'Volunteer button'),
            ('ui-about-btn-partner', 'Partner With Us button'),
        ],
    ),
    (
        'contact',
        'Contact page',
        'Text on the contact page.',
        [
            ('ui-contact-title', 'Page title'),
            ('ui-contact-lead', 'Introduction paragraph'),
            ('ui-contact-label-address', 'Address label'),
            ('ui-contact-label-phone', 'Phone label'),
            ('ui-contact-label-email', 'Email label'),
            ('ui-contact-label-hours', 'Hours label'),
            ('contact-preview-note', 'Preview note (staff only)'),
        ],
    ),
    (
        'donate',
        'Donate page',
        'Text on the donation page.',
        [
            ('donate-intro', 'Introduction above the donate button'),
            ('donate-zeffy-info', 'Zeffy partnership message'),
            ('donate-tax-body', 'Tax deductible paragraph'),
            ('ui-donate-title', 'Page title'),
            ('ui-donate-section-title', 'Donation section heading'),
            ('ui-donate-btn', 'Donate Now button'),
            ('ui-donate-other-ways', 'Other ways to give heading'),
            ('ui-donate-tax-heading', 'Tax deductible heading'),
        ],
    ),
    (
        'site',
        'Site-wide (navigation & footer)',
        'Labels and text shown on every page.',
        [
            ('ui-nav-home', 'Navigation: Home'),
            ('ui-nav-about', 'Navigation: About'),
            ('ui-nav-events', 'Navigation: Events'),
            ('ui-nav-resources', 'Navigation: Resources'),
            ('ui-nav-contact', 'Navigation: Contact'),
            ('ui-nav-donate', 'Navigation: Donate'),
            ('footer-tagline', 'Short tagline in the footer'),
            ('contact-email', 'Contact email address'),
            ('contact-contacts', 'Contact names and phone numbers'),
            ('contact-address', 'Mailing address'),
            ('contact-hours', 'Office and service hours'),
            ('ui-footer-quick-links', 'Footer: Quick Links heading'),
            ('ui-footer-about-us', 'Footer: About Us link'),
            ('ui-footer-contact-info', 'Footer: Contact Info heading'),
            ('ui-footer-rights', 'Footer: All rights reserved'),
            ('ui-footer-staff-login', 'Footer: Staff Login link'),
        ],
    ),
]

CONTENT_LABELS = {
    key: label
    for _id, _title, _help, items in CONTENT_SECTIONS
    for key, label in items
}

SECTION_BY_KEY = {
    key: section_id
    for section_id, _title, _help, items in CONTENT_SECTIONS
    for key, _label in items
}
