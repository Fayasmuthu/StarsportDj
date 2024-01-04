from django.contrib import admin

from main.models import District
from main.models import State


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    pass