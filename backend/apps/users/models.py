from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('farmer', _('Farmer')),
        ('merchant', _('Merchant')),
        ('admin', _('Admin')),
    )
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='farmer',
        verbose_name=_('User Type')
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        verbose_name=_('Phone Number')
    )
    address = models.TextField(
        blank=True,
        verbose_name=_('Address')
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Location')
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        verbose_name=_('Profile Picture')
    )
    bio = models.TextField(
        blank=True,
        verbose_name=_('Bio')
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_('Is Verified')
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Rating')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('user-detail', args=[str(self.id)])

    @property
    def is_farmer(self):
        return self.user_type == 'farmer'

    @property
    def is_merchant(self):
        return self.user_type == 'merchant'

    @property
    def is_admin(self):
        return self.user_type == 'admin'

    def update_rating(self):
        """Update user rating based on reviews"""
        from apps.marketplace.models import Review
        reviews = Review.objects.filter(user=self)
        if reviews.exists():
            self.rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.save() 