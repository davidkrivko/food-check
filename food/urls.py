from django.urls import path

from food.views import (
    CreateOrderApiView,
    PrintNewChecksApiView,
    ListChecksApiView,
)


urlpatterns = [
    path("create-order/", CreateOrderApiView.as_view()),
    path("print-checks/<str:api_key>/", PrintNewChecksApiView.as_view()),
    path("checks/<int:point_id>/", ListChecksApiView.as_view()),
]
