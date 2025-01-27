from django.db import models
from django.utils.translation import gettext_lazy as _

from ordered_model.models import OrderedModel, OrderedModelManager
from solo.models import SingletonModel
from zgw_consumers.constants import APITypes


class OpenKlantConfigManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("klanten_service", "contactmomenten_service")


class OpenKlantConfig(SingletonModel):
    """
    Global configuration and defaults for Klant & Contactmomenten APIs
    """

    klanten_service = models.OneToOneField(
        "zgw_consumers.Service",
        verbose_name=_("Klanten API"),
        on_delete=models.PROTECT,
        limit_choices_to={"api_type": APITypes.kc},
        related_name="+",
        null=True,
        blank=True,
    )
    contactmomenten_service = models.OneToOneField(
        "zgw_consumers.Service",
        verbose_name=_("Contactmomenten API"),
        on_delete=models.PROTECT,
        limit_choices_to={"api_type": APITypes.cmc},
        related_name="+",
        null=True,
        blank=True,
    )

    register_email = models.EmailField(
        verbose_name=_("Registreer op email adres"),
        blank=True,
    )
    register_contact_moment = models.BooleanField(
        verbose_name=_("Registreer in Contactmomenten API"),
        default=False,
    )
    register_bronorganisatie_rsin = models.CharField(
        verbose_name=_("Organisatie RSIN"),
        max_length=9,
        default="",
        blank=True,
    )
    register_type = models.CharField(
        verbose_name=_("Contactmoment type"),
        max_length=50,
        default="Melding",  # 'Melding' is the default
        blank=True,
        help_text=_("Naam van 'contacttype' uit e-Suite"),
    )
    register_employee_id = models.CharField(
        verbose_name=_("Medewerker identificatie"),
        max_length=24,
        default="",
        blank=True,
        help_text=_("Gebruikersnaam van actieve medewerker uit e-Suite"),
    )

    register_api_required_fields = (
        "register_contact_moment",
        "contactmomenten_service",
        "klanten_service",
        "register_bronorganisatie_rsin",
        "register_type",
        "register_employee_id",
    )

    objects = OpenKlantConfigManager()

    class Meta:
        verbose_name = _("Open Klant configuration")

    def has_register(self) -> bool:
        return self.register_email or self.has_api_configuration()

    def has_form_configuration(self) -> bool:
        return self.has_register() and self.contactformsubject_set.exists()

    def has_api_configuration(self):
        return all(getattr(self, f, "") for f in self.register_api_required_fields)


class ContactFormSubject(OrderedModel):
    subject = models.CharField(
        verbose_name=_("Onderwerp"),
        max_length=255,
    )
    # FK for easy inline admins
    config = models.ForeignKey(
        OpenKlantConfig,
        on_delete=models.CASCADE,
    )

    order_with_respect_to = "config"

    objects = OrderedModelManager()

    class Meta(OrderedModel.Meta):
        verbose_name = _("Contact formulier onderwerp")
        verbose_name_plural = _("Contact formulier onderwerpen")
        ordering = ("order",)

    def __str__(self):
        return self.subject
