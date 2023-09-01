from django.contrib import admin
from .models import CheckModel, PrinterModel


class CheckAdmin(admin.ModelAdmin):
    list_filter = ("printer", "status", "type")


class PrinterAdmin(admin.ModelAdmin):
    list_filter = ("check_type", "point_id")


admin.site.register(CheckModel, CheckAdmin)
admin.site.register(PrinterModel, PrinterAdmin)
