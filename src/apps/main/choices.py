from django.db import models
from django.utils.translation import gettext_lazy as _


class AccessPermissionRoleChoices(models.TextChoices):
    GOB_COUNCIL_DRIVING_GROUP = "GC", _("Governing Council and Driving Group")
    ALL_USERS = "AU", _("All users")


class TagsChoices(models.TextChoices):
    GENERAL_ASSEMBLY = "GA", _("General Assembly")
    ACTS = "AC", _("Acts")
    BUDGETS_INVOICES = "BI", _("Budgets and invoices")
    CORPORATE = "CO", _("Corporate")


class ProjectStatusChoices(models.TextChoices):
    PROJECT_STUDY_PHASE = "PS", _("Project in study phase")
    PROJECT_DEVELOPMENT = "AP", _("Active Project")
    OTHER_PROJECTS = "OP", _("Future projects or other projects")
