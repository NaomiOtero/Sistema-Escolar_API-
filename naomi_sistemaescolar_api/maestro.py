from django.contrib import admin
from django.utils.html import format_html
from naomi_sistemaescolar_api.models import *


@admin.register(Maestros)

class MaestrosAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "creation", "update")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")

