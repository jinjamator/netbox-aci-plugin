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


class ACIAppProfile(NetBoxModel):
    """NetBox model for ACI Application Profile."""

    name = models.CharField(
        max_length=64,
        validators=[
            MaxLengthValidator(64),
            ACIPolicyNameValidator,
        ],
        verbose_name=_("name"),
    )
    alias = models.CharField(
        max_length=64,
        blank=True,
        validators=[ACIPolicyNameValidator],
        verbose_name=_("alias"),
    )
    description = models.CharField(
        max_length=128,
        blank=True,
        validators=[ACIPolicyDescriptionValidator],
        verbose_name=_("description"),
    )
    aci_tenant = models.ForeignKey(
        to=ACITenant,
        on_delete=models.PROTECT,
        related_name="aci_app_profiles",
        verbose_name=_("ACI Tenant"),
    )
    nb_tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="+",
        blank=True,
        null=True,
        verbose_name=_("NetBox tenant"),
    )
    comments = models.TextField(
        blank=True,
        verbose_name=_("comments"),
    )

    class Meta:
        ordering: tuple = ("aci_tenant", "name")
        unique_together: tuple = ("aci_tenant", "name")
        verbose_name: str = _("ACI Application Profile")

    def __str__(self) -> str:
        """Return string representation of the instance."""
        return self.name

    def get_absolute_url(self) -> str:
        """Return the absolute URL of the instance."""
        return reverse(
            "plugins:netbox_aci_plugin:aciappprofile", args=[self.pk]
        )
