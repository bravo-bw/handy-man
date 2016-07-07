from django.contrib import admin

from django.contrib.admin import ModelAdmin

from ..models import District, TownVillage, Street


class DistrictAdmin(ModelAdmin):

    list_filter = ['district_name']

    list_display = ['district_name', 'center_latitude', 'center_longitude']

    search_fields = ['district_name']

admin.site.register(District, DistrictAdmin)


class TownVillageAdmin(ModelAdmin):

    list_filter = ['district', 'town_village_name']

    list_display = ['district', 'town_village_name', 'center_latitude', 'center_longitude']

    search_fields = ['district', 'town_village_name']

admin.site.register(TownVillage, TownVillageAdmin)


class StreetAdmin(ModelAdmin):

    list_filter = ['town_village', 'street_name']

    list_display = ['town_village', 'street_name', 'center_latitude', 'center_longitude']

    search_fields = ['town_village', 'street_name']

admin.site.register(Street, StreetAdmin)
