from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser, PermissionsMixin):
    class UserRole(models.TextChoices):
        SYSTEM_ADMIN = "SYSTEM_ADMIN", _("system admin")
        NORMAL_USER = "NORMAL_USER", _("normal user")

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"), max_length=150, unique=True, validators=[username_validator], db_index=True
    )
    first_name = models.CharField(verbose_name=_("name"), max_length=32, default="")
    last_name = models.CharField(verbose_name=_("last name"), max_length=64, null=True, blank=True)
    phone_number = models.CharField(
        verbose_name=_("phone number"),
        validators=[RegexValidator(regex="^(?:(?:\+|00)88|01)?\d{11}$")],
        max_length=16,
        unique=False,
        db_index=True,
    )
    email = models.EmailField(verbose_name=_("email address"), null=True, blank=True)
    role = models.CharField(
        verbose_name=_("role"),
        max_length=16,
        choices=UserRole.choices,
        default=UserRole.NORMAL_USER,
        help_text=_("role designates user's role at the time it could has only one role "),
    )
    address = models.TextField(verbose_name="address")

    def __str__(self):
        return _(f"{self.first_name} {self.phone_number}")

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.phone_number

        return super().save(*args, **kwargs)
