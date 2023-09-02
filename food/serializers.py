from rest_framework import serializers

from food.models import CheckModel


class DishSerializer(serializers.Serializer):
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.FloatField()


class OrderSerializer(serializers.Serializer):
    dishes = DishSerializer(many=True)
    id = serializers.IntegerField()
    point = serializers.IntegerField()
    total = serializers.FloatField(
        required=False,
        help_text="This field is calculated when creating a check"
    )


class CheckCreateSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = CheckModel
        fields = ("order",)


class CheckModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckModel
        fields = ("id", "type", "status")


class CheckDetailSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = CheckModel
        fields = ("id", "type", "status", "order",)
