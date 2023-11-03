"""

Django admin customization

"""

from typing import Any
from django.contrib import admin
from django.core.paginator import Paginator
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):

    """Define the aadmin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None,{'fields':('name','email','password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                )
            }
        ),
        (_('Important dates'),{'fields':('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            "classes": ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
            ),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        return self.fieldsets


class HistoricAdmin(admin.ModelAdmin):
    """Admin panel for HistoryAdmin"""
    ordering = ['-id']
    list_display = ['id','invoice']
    list_per_page = 50

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        
        # Check if the field has null=True and default=None
        if field and db_field.null and db_field.default is None:
            field.required = False  # Set the field as not required

        return field 
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request).only('id', 'invoice').defer(*[f.name for f in self.model._meta.get_fields() if f.name not in ['id', 'invoice']])
        return queryset

    def get_paginator(self, request, queryset, per_page, orphans=0,
                      allow_empty_first_page=True, **kwargs):
        # Use a custom paginator to optimize retrieval
        paginator = Paginator(queryset, per_page, orphans=orphans,
                              allow_empty_first_page=allow_empty_first_page,
                              **kwargs)

        return paginator

class TariffAdmin(admin.ModelAdmin):
    """Tarrif view for admin."""
    ordering = ['-id']
    list_display = ['id','country','retail_handling_cost','domestic_linehaul_cost']
    list_per_page = 50

class RiepilogoAdmin(admin.ModelAdmin):
    """Admin panel for riepilogo table"""
    list_display = ['id']
    list_per_page = 50

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        
        # Check if the field has null=True and default=None
        if field and db_field.null and db_field.default is None:
            field.required = False  # Set the field as not required

        return field 

class RiepilogoColumnAccessAdmin(admin.ModelAdmin):
    """Admin panel for access control list"""
    list_display = ['group', 'column']
    list_per_page = 50

class TariffPerCartonAdmin(admin.ModelAdmin):
    """Admin panel for tariffs."""
    list_display = ["country", "city", "tariff"]
    list_per_page = 50


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Historic, HistoricAdmin)
admin.site.register(models.Tariff, TariffAdmin)
admin.site.register(models.Riepilogo, RiepilogoAdmin)
admin.site.register(models.RiepilogoColumnAccess, RiepilogoColumnAccessAdmin)
admin.site.register(models.TariffPerCaton, TariffPerCartonAdmin)
admin.site.register(models.TARIFFE)
admin.site.register(models.WHOLESALE_TARIFFE)
admin.site.register(models.tblSocInvoicing)
admin.site.register(models.WHL_DISTRIBUTION_N)
admin.site.register(models.DESTINATION_N)
