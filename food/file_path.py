import os

from django.conf import settings


def get_pdf_file_path(instance, filename=None):
    return os.path.join(
        settings.MEDIA_ROOT,
        "pdf",
        f"{instance.order['id']}_{instance.get_type_display()}.pdf",
    )
