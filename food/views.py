from rest_framework import status, views, generics
from rest_framework.response import Response

from food.models import CheckModel, PrinterModel
from food.serializers import (
    CheckCreateSerializer,
    CheckModelSerializer,
    CheckDetailSerializer,
)
from food.utils import create_checks_for_order


class ListChecksApiView(generics.ListAPIView):
    serializer_class = CheckModelSerializer

    def get_queryset(self):
        point_id = self.kwargs["point_id"]
        return CheckModel.objects.filter(printer__point_id=point_id)


class RetrieveChecksApiView(generics.RetrieveAPIView):
    serializer_class = CheckDetailSerializer
    queryset = CheckModel.objects.all()


class CreateOrderApiView(generics.CreateAPIView):
    queryset = CheckModel.objects.all()
    serializer_class = CheckCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            order = serializer.validated_data.get("order")
            point = order["point"]

            printers = PrinterModel.objects.filter(point_id=point)

            if not printers:
                return Response(
                    {"error": f"No printers for point {point}"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            checks = CheckModel.objects.filter(order__id=order["id"])
            if checks:
                return Response(
                    {"error": "Check already exist!"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            res_checks = create_checks_for_order(order, printers)

            output_serializer = CheckModelSerializer(res_checks, many=True)
            response = {
                "message": "Checks processed!",
                "data": output_serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrintNewChecksApiView(views.APIView):
    def get(self, request, api_key):
        # Fetch new checks for the given printer
        checks = CheckModel.objects.filter(
            printer__api_key=api_key,
            status="rendered"
        )
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
        """
        Logic to send pdf_content to the
        printer using printer's API or driver
        """
        pass

    def print_check(self, check):
        pdf_content = self.get_pdf_content(check)
        self.send_to_printer(check.printer, pdf_content)
        check.status = "printed"
        check.save()
