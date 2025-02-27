from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """Custom user model for the Libro application."""

    # Additional fields
    phone_number = models.CharField(
        _("phone number"),
        max_length=15,
        blank=True,
        help_text=_("Contact phone number"),
    )

    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)

    address = models.TextField(_("address"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username 
