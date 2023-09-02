from rest_framework import status, views, generics
from rest_framework.response import Response

from food.models import CheckModel
from food.serializers import CheckCreateModelSerializer, CheckModelSerializer
from food.utils import create_check_for_order, select_printer_for_order


class ListChecksApiView(generics.ListAPIView):
    serializer_class = CheckModelSerializer

    def get_queryset(self):
        point_id = self.kwargs["point_id"]
        return CheckModel.objects.filter(printer__point_id=point_id)


class CreateOrderApiView(views.APIView):
    def post(self, request):
        serializer = CheckCreateModelSerializer(data=request.data)

        if serializer.is_valid():
            order = serializer.validated_data.get("order")
            printers = select_printer_for_order(order)

            if not printers:
                return Response(
                    {"error": f"No printers for point {order['point']}"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            checks = CheckModel.objects.filter(order__id=order["id"])
            if checks:
                return Response(
                    {"error": "Check already exist!"}, status=status.HTTP_403_FORBIDDEN
                )

            res_checks = create_check_for_order(order)

            serializer = CheckModelSerializer(res_checks, many=True)
            response = {"message": "Checks processed!", "data": serializer.data}
            return Response(response, status=status.HTTP_201_CREATED)


class PrintNewChecksApiView(views.APIView):
    def get(self, request, api_key):
        # Fetch new checks for the given printer
        checks = CheckModel.objects.filter(printer__api_key=api_key, status="rendered")
        for check in checks:
            self.print_check(check)

        serializer = CheckModelSerializer(checks, many=True)

        response = {
            "message": "Successfully create checks!",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def get_pdf_content(self, check):
        with open(check.pdf_file.path, "rb") as pdf:
            return pdf.read()

    def send_to_printer(self, printer, pdf_content):
        # Logic to send pdf_content to the printer using printer's API or driver
        pass

    def print_check(self, check):
        pdf_content = self.get_pdf_content(check)
        self.send_to_printer(check.printer, pdf_content)
        check.status = "printed"
        check.save()
