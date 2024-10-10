from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from apps.users.forms import CustomUserCreationForm, UserAdminForm
from apps.users.models import User, UserCharge
from apps.users.services import ExportUserCsvMixin
from project.admin import ModelAdminMixin


@admin.register(UserCharge)
class UserChargeAdmin(admin.ModelAdmin):
    fields = ("name",)
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(User)
class UserAdmin(ModelAdminMixin, BaseUserAdmin, ExportUserCsvMixin):
    form = UserAdminForm
    add_form = CustomUserCreationForm
    list_display = (
        "full_name",
        "dni",
        "email",
        "charge",
        "is_staff",
    )
    list_filter = (
        "charge",
        "is_staff",
        "governing_council_member",
    )
    search_fields = ("email", "name", "surnames", "charge", "dni")
    ordering = ("name",)
    fieldsets = (("Autenticació", {"fields": ("dni", "password")}),)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            "Autenticació",
            {"classes": ("wide",), "fields": ("dni", "password1", "password2")},
        ),
    )
    # common_fieldsets is not a standard ModelAdmin attribute. We extend
    # get_fieldsets to avoid having to repeat info in fieldsets and add_fieldsets.
    common_fieldsets = (
        (
            "Dades",
            {
                "fields": (
                    "name",
                    "surnames",
                    "phone",
                    "address",
                    "email",
                    "email_verified",
                    "bank_account",
                    "charge",
                    "governing_council_member",
                    "projects",
                    "partner_id",
                    "entry_year",
                    "corporate_contribution",
                    "voluntary_contribution",
                )
            },
        ),
        (
            "Permisos i autoritzacions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "roles_explanation_field",
                    "groups",
                ),
            },
        ),
        (
            "Registre",
            {
                "fields": (
                    "created_by",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    superuser_fields = ("is_superuser",)
    readonly_fields = ("roles_explanation_field",)
    actions = ["export_as_csv"]

    def get_fieldsets(self, request, obj=None):
        return super().get_fieldsets(request, obj) + self.common_fieldsets

    @admin.display(description="Informació rols d'usuari")
    def roles_explanation_field(self, obj):
        return format_html(
            """
            <ul>
              <li>Admins: accés a la configuració i personalització del
                backoffice, al llistat d'emails enviats pel sistema i a les
                plantilles de les notificacions. També pot editar els camps
                "Is staff" i "Is active" de la fitxa d'usuaris.
              </li>
            </ul>
            """
        )
