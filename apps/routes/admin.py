from django.contrib import admin
from django import forms

from . import models


class RouteStopInline(admin.TabularInline):
    model = models.RouteStop
    raw_id_fields = ['stop', 'route', 'next_stop']
    ordering = ['order', 'stop__name']
    fields = ['order', 'stop']


class RouteAdminForm(forms.ModelForm):

    class Meta:
        model = models.Route
        fields = "__all__"


class RouteAdmin(admin.ModelAdmin):
    form = RouteAdminForm
    list_display = [
        "name",
        "display_name",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]
    inlines = [
        RouteStopInline,
    ]
    ordering = ['name']


class StopAdminForm(forms.ModelForm):

    class Meta:
        model = models.Stop
        fields = "__all__"


class StopAdmin(admin.ModelAdmin):
    search_fields = [
        '~name',
        'name',
    ]
    form = StopAdminForm
    list_display = [
        "name",
        "lon",
        "lat",
        "address",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]
    inlines = [
        RouteStopInline,
    ]

    def get_search_results(self, request, queryset, search_term):
        """
        Return a tuple containing a queryset to implement the search
        and a boolean indicating if the results may contain duplicates.
        """

        # Apply keyword searches.
        def construct_search(field_name):
            from django.core.exceptions import FieldDoesNotExist
            from django.db.models.constants import LOOKUP_SEP

            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            elif field_name.startswith('~'):
                return "%s__trigram_similar" % field_name[1:]
            # Use field_name if it includes a lookup.
            opts = queryset.model._meta
            lookup_fields = field_name.split(LOOKUP_SEP)
            # Go through the fields, following all relations.
            prev_field = None
            for path_part in lookup_fields:
                if path_part == 'pk':
                    path_part = opts.pk.name
                try:
                    field = opts.get_field(path_part)
                except FieldDoesNotExist:
                    # Use valid query lookups.
                    if prev_field and prev_field.get_lookup(path_part):
                        return field_name
                else:
                    prev_field = field
                    if hasattr(field, 'get_path_info'):
                        # Update opts to follow the relation.
                        opts = field.get_path_info()[-1].to_opts
            # Otherwise, use the field with icontains.
            return "%s__icontains" % field_name

        import operator
        from functools import reduce
        from django.contrib.admin.utils import lookup_needs_distinct
        from django.db.models import Q

        use_distinct = False
        search_fields = self.get_search_fields(request)
        if search_fields and search_term:
            orm_lookups = [construct_search(str(search_field))
                           for search_field in search_fields]
            for bit in search_term.split():
                or_queries = [Q(**{orm_lookup: bit})
                              for orm_lookup in orm_lookups]
                queryset = queryset.filter(reduce(operator.or_, or_queries))
            use_distinct |= any(lookup_needs_distinct(self.opts, search_spec) for search_spec in orm_lookups)

        return queryset, use_distinct


admin.site.register(models.Route, RouteAdmin)
admin.site.register(models.Stop, StopAdmin)
