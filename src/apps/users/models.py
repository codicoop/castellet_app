from django.contrib import admin
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.main.models import Project
from project.fields import flowbite
from project.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, password
        and extra fields.
        """
        if not email:
            raise ValueError(_("Users must have an email address"))

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email, password
        and extra fields.
        """
        if not password:
            raise ValueError(_("Superusers must have a password"))

        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    name = flowbite.ModelCharField(
        _("name"),
        max_length=50,
        blank=False,
        null=False,
    )
    surnames = flowbite.ModelCharField(
        _("surname"),
        max_length=50,
        blank=False,
        null=False,
    )
    email = flowbite.ModelEmailField(
        _("email address"),
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    email_verification_code = models.CharField(default="0000")
    email_verified = models.BooleanField(default=False)
    phone = flowbite.ModelCharField(
        _("Contact telephone"),
        max_length=20,
        blank=True,
        null=True,
    )
    address = flowbite.ModelCharField(
        _("Address"),
        max_length=255,
        blank=True,
        null=True,
    )
    dni = flowbite.ModelCharField(
        _("National Identity Document"),
        max_length=10,
        blank=True,
        null=True,
    )
    bank_account = flowbite.ModelCharField(
        _("Bank account"),
        max_length=24,
        blank=True,
        null=True,
    )
    charge = flowbite.ModelCharField(
        _("Charge"),
        max_length=50,
        blank=True,
        null=True,
    )
    governing_council_member = flowbite.ModelBooleanField(
        _("Is governing council member"),
        default=False,
        blank=True,
        null=True,
        help_text=_("Is this user a governing council member?"),
    )
    projects = models.ManyToManyField(
        Project,
        blank=True,
        null=True,
        related_name="user_projects",
        verbose_name=_("Projects"),
    )
    partner_id = flowbite.ModelCharField(
        _("Partner ID"),
        max_length=50,
        blank=True,
        null=True,
    )
    entry_year = flowbite.ModelCharField(
        _("Entry year"),
        max_length=4,
        blank=True,
        null=True,
    )
    corporate_contribution = flowbite.ModelCharField(
        _("Corporate contribution"),
        max_length=10,
        blank=True,
        null=True,
    )
    voluntary_contribution = flowbite.ModelCharField(
        _("Voluntary contribution"),
        max_length=10,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(_("Is staff"), default=True)
    is_staff = models.BooleanField(_("Is active"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name

    @property
    @admin.display(
        ordering="name",
        description=_("name"),
    )
    def full_name(self):
        return f"{self.name} {self.surnames}".strip()

    def has_admin_role(self):
        return self.is_staff or self.is_superuser

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
