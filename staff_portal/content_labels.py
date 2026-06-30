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
        ],
    ),
    (
        'donate',
        'Donate page',
        'Text on the donation page.',
        [
            ('donate-intro', 'Introduction above the donate button'),
        ],
    ),
    (
        'site',
        'Contact & footer',
        'Email, phone, and footer text shown on every page.',
        [
            ('footer-tagline', 'Short tagline in the footer'),
            ('contact-email', 'Contact email address'),
            ('contact-phone', 'Contact phone number'),
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
