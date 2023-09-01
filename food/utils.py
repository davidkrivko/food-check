import base64
import httpx

from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
from channels.db import database_sync_to_async

from food.file_path import get_pdf_file_path
from food.models import CheckModel, PrinterModel


WKHTMLTOPDF_SERVICE_URL = "http://localhost:8080/"


async def generate_pdf(instance):
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

    async with httpx.AsyncClient() as client:
        response = await client.post(WKHTMLTOPDF_SERVICE_URL, json=payload, headers=headers)

        if response.status_code == 200:
            dest_pdf_path = get_pdf_file_path(instance)

            with open(dest_pdf_path, "wb") as pdf_file:
                pdf_file.write(response.content)

            # Use database_sync_to_async to handle database update
            await update_instance_pdf_file(instance, dest_pdf_path)
        else:
            print(f"wkhtmltopdf service error: {response.content}")


@database_sync_to_async
def update_instance_pdf_file(instance, dest_pdf_path):
    instance.pdf_file = dest_pdf_path
    instance.status = "rendered"
    instance.save()


def create_check_for_order(order):
    # Calculate the total for the order
    order["total"] = sum(dish["amount"] * dish["price"] for dish in order["dishes"])

    # Logic to select a printer. This can be adjusted as per your needs.
    printers = select_printer_for_order(order)

    # Create check for the selected printer
    res = []
    for printer in printers:
        check = CheckModel.objects.create(
            type=printer.check_type,
            printer=printer,
            order=order,
        )
        res.append(check)

        # Generate PDF for the check
        async_to_sync(generate_pdf)(check)

    return res


def select_printer_for_order(order):
    return [
        PrinterModel.objects.filter(point_id=order["point"], check_type="client").first(),
        PrinterModel.objects.filter(point_id=order["point"], check_type="kitchen").first(),
    ]
