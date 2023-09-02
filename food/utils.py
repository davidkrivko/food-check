from food.models import CheckModel, PrinterModel
from food.tasks import generate_pdf


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

        generate_pdf.delay(check.id)

    return res


def select_printer_for_order(order):
    point = order["point"]

    printers = list(PrinterModel.objects.filter(point_id=point))

    if not printers:
        return []

    client_printer = next(
        (printer for printer in printers if printer.check_type == "client"), None
    )
    kitchen_printer = next(
        (printer for printer in printers if printer.check_type == "kitchen"), None
    )

    return [client_printer, kitchen_printer]
