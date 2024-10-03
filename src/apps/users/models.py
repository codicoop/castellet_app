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


class UserCharge(BaseModel):
    name = models.CharField(_("Charge name"), max_length=50)

    def __str__(self):
        return self.name

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    name = flowbite.ModelCharField(
        _("name"),
        max_length=50,
        blank=False,
        default=""
    )
    surnames = flowbite.ModelCharField(
        _("surname"),
        max_length=50,
        blank=False,
        default=""
    )
    email = flowbite.ModelEmailField(
        _("email address"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("If this field is empty a default email will be added.")
    )
    phone = flowbite.ModelCharField(
        _("Contact telephone"),
        max_length=20,
        blank=True,
        default=""
    )
    address = flowbite.ModelCharField(
        _("Address"),
        max_length=255,
        blank=True,
        default=""
    )
    dni = flowbite.ModelCharField(
        _("National Identity Document"),
        max_length=10,
        blank=False,
        default="",
        unique=True
    )
    bank_account = flowbite.ModelCharField(
        _("Bank account"),
        max_length=24,
        blank=True,
        default=""
    )
    charge = models.ForeignKey(
        UserCharge,
        on_delete=models.SET_NULL,
        related_name="user_charge",
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
        related_name="user_projects",
        verbose_name=_("Projects"),
    )
    partner_id = flowbite.ModelCharField(
        _("Partner ID"),
        max_length=50,
        blank=True,
        default=""
    )
    entry_year = flowbite.ModelCharField(
        _("Entry year"),
        max_length=4,
        blank=True,
        default=""
    )
    corporate_contribution = flowbite.ModelCharField(
        _("Corporate contribution"),
        max_length=10,
        blank=True,
        default=""
    )
    voluntary_contribution = flowbite.ModelCharField(
        _("Voluntary contribution"),
        max_length=10,
        blank=True,
        default=""
    )
    is_active = models.BooleanField(_("Is staff"), default=True)
    is_staff = models.BooleanField(_("Is active"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "dni"
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

    def clean(self):
        super().clean()
        print(self.email)
        if not self.email:
            self.email = "codi@codi.coop"