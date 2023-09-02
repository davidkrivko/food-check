import base64
import os

import requests
from django.template.loader import render_to_string

from food.file_path import get_pdf_file_path
from food.models import CheckModel
from food_service.celery import app
from food_service.settings import WKHTMLTOPDF_SERVICE_URL, MEDIA_ROOT


@app.task
def generate_pdf(check_id):
    try:
        instance = CheckModel.objects.get(pk=check_id)
    except:
        return

    if instance.status == "rendered":
        return

    if instance.type == "client":
        rendered_html = render_to_string("checks/client_pattern.html", {"order": instance.order})
    elif instance.type == "kitchen":
        rendered_html = render_to_string("checks/kitchen_pattern.html", {"order": instance.order})
    else:
        return

    encoded_html = base64.b64encode(rendered_html.encode('utf-8')).decode('utf-8')

    payload = {"contents": encoded_html}
    headers = {"Content-Type": "application/json"}

    response = requests.post(WKHTMLTOPDF_SERVICE_URL, json=payload, headers=headers)

    if response.status_code == 200:
        relative_path = get_pdf_file_path(instance)
        dest_pdf_path = os.path.join(MEDIA_ROOT, relative_path)

        with open(dest_pdf_path, "wb") as pdf_file:
            pdf_file.write(response.content)

        instance.pdf_file = relative_path
        instance.status = "rendered"
        instance.save()
    else:
        print(f"wkhtmltopdf service error: {response.content}")
