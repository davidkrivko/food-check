from django.db import models

from food.choices import CHECK_TYPE, STATUS_CHOICES
from food.file_path import get_pdf_file_path


class PrinterModel(models.Model):
    name = models.CharField(max_length=64)
    api_key = models.CharField(unique=True, max_length=256)
    check_type = models.CharField(choices=CHECK_TYPE)
    point_id = models.IntegerField()

    def __str__(self):
        return f"id: {self.id} | key: {self.api_key} | point: {self.point_id}"


class CheckModel(models.Model):
    type = models.CharField(choices=CHECK_TYPE)
    status = models.CharField(
        choices=STATUS_CHOICES,
        default="new",
    )
    order = models.JSONField()
    printer = models.ForeignKey(
        "PrinterModel", on_delete=models.CASCADE, related_name="checks"
    )

    pdf_file = models.FileField(
        upload_to=get_pdf_file_path,
        null=True,
        blank=True,
    )

    def __str__(self):
        return (
            f"id: {self.id} |"
            f"order: {self.order['id']} |"
            f"printer: {self.printer.api_key}"
        )
