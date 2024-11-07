from django.contrib import admin
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.partners.models import Project
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

    class Meta:
        verbose_name = _("charge")
        verbose_name_plural = _("charges")

    def __str__(self):
        return self.name


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_("name"), max_length=50, blank=False, default="")
    surnames = models.CharField(_("surname"), max_length=50, blank=False, default="")
    email = models.EmailField(
        _("email address"),
        max_length=255,
        blank=True,
        null=True,
        unique=True,
    )
    email_verification_code = models.CharField(default="0000")
    email_verified = models.BooleanField(default=False)
    phone = models.CharField(
        _("Contact telephone"), max_length=20, blank=True, default=""
    )
    address = models.CharField(_("Address"), max_length=255, blank=True, default="")
    dni = models.CharField(
        _("National Identity Document"),
        max_length=10,
        blank=False,
        default="",
        unique=True,
    )
    bank_account = models.CharField(
        _("Bank account"), max_length=24, blank=True, default=""
    )
    charge = models.ForeignKey(
        UserCharge,
        on_delete=models.SET_NULL,
        related_name="user_charge",
        verbose_name=_("charge"),
        blank=True,
        null=True,
    )
    governing_council_member = models.BooleanField(
        _("Is governing council member"),
        default=False,
        blank=True,
        null=True,
    )
    projects = models.ManyToManyField(
        Project,
        blank=True,
        related_name="user_projects",
        verbose_name=_("Projects"),
    )
    partner_id = models.CharField(
        _("Partner ID"), max_length=50, blank=True, default=""
    )
    entry_year = models.CharField(_("Entry year"), max_length=4, blank=True, default="")
    corporate_contribution = models.CharField(
        _("Corporate contribution"), max_length=10, blank=True, default=""
    )
    voluntary_contribution = models.CharField(
        _("Voluntary contribution"), max_length=10, blank=True, default=""
    )
    is_active = models.BooleanField(_("Is active"), default=True)
    is_staff = models.BooleanField(_("Is staff"), default=False)

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

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if not self.email:
            self.email_verified = True
            self.email = None
            super(User, self).save(*args, **kwargs)

    def clean(self):
        if self.pk and self.email:
            try:
                old_email= User.objects.get(pk=self.pk).email
                if old_email != self.email:
                    self.email_verified = False
            except Exception:
                pass
