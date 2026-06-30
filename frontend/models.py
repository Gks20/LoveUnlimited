from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class ResourceCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    icon_class = models.CharField(max_length=60, blank=True, help_text="Optional FontAwesome icon class")
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordering", "name"]
        verbose_name = "Resource Category"
        verbose_name_plural = "Resource Categories"

    def __str__(self):
        return self.name


class Resource(models.Model):
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE, related_name="resources")
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    website = models.URLField(blank=True)
    hours = models.CharField(max_length=120, blank=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords")
    is_active = models.BooleanField(default=True)
    ordering = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category__ordering", "ordering", "name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["category", "is_active"]),
        ]

    def __str__(self):
        return self.name

    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]


class SiteContent(models.Model):
    LANGUAGE_CHOICES = [('en', 'English'), ('es', 'Español')]

    key = models.SlugField(max_length=80)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    title = models.CharField(max_length=200, blank=True, help_text="Admin label / optional heading")
    body = models.TextField()

    class Meta:
        unique_together = [('key', 'language')]
        ordering = ['key', 'language']
        verbose_name = 'Site content block'
        verbose_name_plural = 'Site content blocks'

    def __str__(self):
        return f'{self.key} ({self.language})'

    @classmethod
    def get_text(cls, key, language='en', default=''):
        try:
            return cls.objects.get(key=key, language=language).body
        except cls.DoesNotExist:
            return default


class Post(models.Model):
    LANGUAGE_CHOICES = [('en', 'English'), ('es', 'Español')]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    featured_image = models.ImageField(upload_to='posts/', blank=True, null=True)
    related_event = models.ForeignKey(
        'calendar_app.Event', on_delete=models.SET_NULL, null=True, blank=True, related_name='posts'
    )
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']
        unique_together = [('slug', 'language')]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)


class DonationSettings(models.Model):
    zeffy_form_link = models.URLField(
        max_length=500,
        default='https://www.zeffy.com/embed/donation-form/donate-to-change-lives-416?modal=true',
        help_text='Zeffy modal form URL used on donate buttons (zeffy-form-link).',
    )
    zeffy_embed_html = models.TextField(
        blank=True,
        help_text='Optional legacy iframe embed HTML from Zeffy dashboard.',
    )
    tax_id = models.CharField(max_length=50, blank=True)
    impact_25 = models.CharField(max_length=200, default='Provides meals for 5 people')
    impact_50 = models.CharField(max_length=200, default='Supplies hygiene kits for 10 families')
    impact_100 = models.CharField(max_length=200, default='Provides emergency shelter for one night')

    class Meta:
        verbose_name = 'Donation settings'
        verbose_name_plural = 'Donation settings'

    def __str__(self):
        return 'Donation settings'

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=160, help_text='Title or position')
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    ordering = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['ordering', 'name']
        verbose_name = 'Team member'
        verbose_name_plural = 'Team members'

    def __str__(self):
        return self.name

    @property
    def has_photo(self):
        return bool(self.photo)

    @property
    def avatar_icon_class(self):
        """Font Awesome icon when no photo is uploaded — based on role/title."""
        role = self.role.lower()
        if any(term in role for term in ('executive director', 'president', 'ceo', 'founder')):
            return 'fa-user-tie'
        if 'vice president' in role or 'vice-president' in role:
            return 'fa-user-tie'
        if any(term in role for term in ('treasurer', 'finance', 'accounting')):
            return 'fa-calculator'
        if any(term in role for term in ('secretary', 'clerk')):
            return 'fa-pen-fancy'
        if any(term in role for term in ('program', 'outreach', 'volunteer', 'coordinator')):
            return 'fa-hands-helping'
        if 'director' in role:
            return 'fa-user-tie'
        return 'fa-user'
