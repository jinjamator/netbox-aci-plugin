# SPDX-FileCopyrightText: 2024 Martin Hauser
#
# SPDX-License-Identifier: GPL-3.0-or-later

from django.core.validators import MaxLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from netbox.models import NetBoxModel

from ..models.tenants import ACITenant
from ..validators import ACIPolicyDescriptionValidator, ACIPolicyNameValidator


class ACIContractFilter(NetBoxModel):
    """NetBox model for ACI Contract Filter."""

    name = models.CharField(
        verbose_name=_("name"),
        max_length=64,
        validators=[
            MaxLengthValidator(64),
            ACIPolicyNameValidator,
        ],
    )
    name_alias = models.CharField(
        verbose_name=_("name alias"),
        max_length=64,
        blank=True,
        validators=[
            MaxLengthValidator(64),
            ACIPolicyNameValidator,
        ],
    )
    description = models.CharField(
        verbose_name=_("description"),
        max_length=128,
        blank=True,
        validators=[
            MaxLengthValidator(128),
            ACIPolicyDescriptionValidator,
        ],
    )
    aci_tenant = models.ForeignKey(
        to=ACITenant,
        on_delete=models.PROTECT,
        related_name="aci_contract_filters",
        verbose_name=_("ACI Tenant"),
    )
    nb_tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.SET_NULL,
        related_name="aci_contract_filters",
        verbose_name=_("NetBox tenant"),
        blank=True,
        null=True,
    )
    comments = models.TextField(
        verbose_name=_("comments"),
        blank=True,
    )

    clone_fields: tuple = (
        "description",
        "aci_tenant",
        "nb_tenant",
    )
    prerequisite_models: tuple = ("netbox_aci_plugin.ACITenant",)

    class Meta:
        constraints: list[models.UniqueConstraint] = [
            models.UniqueConstraint(
                fields=("aci_tenant", "name"),
                name="unique_aci_contract_filter_name_per_aci_tenant",
            ),
        ]
        ordering: tuple = ("aci_tenant", "name")
        verbose_name: str = _("ACI Contract Filter")

    def __str__(self) -> str:
        """Return string representation of the instance."""
        if self.aci_tenant.name == "common":
            return f"{self.name} ({self.aci_tenant.name})"
        else:
            return self.name

    def get_absolute_url(self) -> str:
        """Return the absolute URL of the instance."""
        return reverse(
            "plugins:netbox_aci_plugin:acicontractfilter", args=[self.pk]
        )
