from rest_framework import serializers

from food.models import CheckModel


class CheckCreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckModel
        fields = ("order",)


class CheckModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckModel
        fields = ("id", "type", "status")
