from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    One Profile per User (OneToOne).
    Auto-created by signal on first Google login.
    Sensitive fields store ENCRYPTED blobs only — never plaintext.
    gmail_configured and gemini_configured are boolean flags only —
    no actual credential value ever stored in plaintext columns.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )

    # Personal info
    full_name    = models.CharField(max_length=100, blank=True)
    phone        = models.CharField(max_length=20, blank=True)
    role         = models.CharField(max_length=150, default='Software Developer')
    skills       = models.TextField(
        default='Python, Django, REST APIs, JavaScript, HTML/CSS, SQL, Git'
    )
    experience_years = models.CharField(max_length=50, blank=True)
    location     = models.CharField(max_length=150, blank=True)
    college      = models.CharField(max_length=200, blank=True)
    grad_year    = models.CharField(max_length=10, blank=True)
    linkedin     = models.URLField(blank=True)
    github       = models.URLField(blank=True)
    portfolio    = models.URLField(blank=True)
    about_me     = models.TextField(blank=True)
    resume       = models.FileField(
        upload_to='resumes/%Y/%m/', blank=True, null=True
    )

    # Encrypted credential blobs — suffix _enc is a reminder these are NOT plaintext
    gmail_enc          = models.TextField(blank=True)
    app_password_enc   = models.TextField(blank=True)
    gemini_key_enc     = models.TextField(blank=True)

    # Boolean status flags — safe to store, no secret value
    gmail_configured   = models.BooleanField(default=False)
    gemini_configured  = models.BooleanField(default=False)

    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'

    def __str__(self):
        return f"{self.display_name}'s Profile"

    @property
    def email(self):
        return self.user.email

    @property
    def display_name(self):
        return (
            self.full_name
            or self.user.get_full_name()
            or self.user.email.split('@')[0].title()
        )

    @property
    def skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    @property
    def initials(self):
        parts = self.display_name.split()
        return (parts[0][0] + (parts[1][0] if len(parts) > 1 else '')).upper()


class EmailLog(models.Model):
    """
    Every sent email is logged here.
    Always filter by user — never expose another user's logs.
    """
    STATUS_CHOICES = [('sent', 'Sent'), ('failed', 'Failed')]

    user           = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='email_logs'
    )
    receiver_email = models.EmailField()
    company_name   = models.CharField(max_length=200)
    theme_used     = models.CharField(max_length=60)
    subject        = models.CharField(max_length=300)
    opening_para   = models.TextField(blank=True)
    ai_used        = models.BooleanField(default=False)
    status         = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='failed'
    )
    error_message  = models.TextField(blank=True)
    sent_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.user.email} → {self.receiver_email} [{self.status}]"


class Company(models.Model):
    """
    Company address book. Scoped per user.
    same email can appear for different users (unique_together handles this).
    """
    user     = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='companies'
    )
    name     = models.CharField(max_length=200)
    email    = models.EmailField()
    notes    = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'email')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} <{self.email}>"
