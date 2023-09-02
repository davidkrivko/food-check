from food.models import CheckModel
from food.tasks import generate_pdf


def create_checks_for_order(order, printers):
    # Calculate the total for the order
    order["total"] = sum(
        dish["quantity"] * dish["price"]
        for dish in order["dishes"]
    )

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
