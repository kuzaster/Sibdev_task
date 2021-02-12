from rest_framework.serializers import FileField, ModelSerializer, Serializer

from .models import Customer


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class FileUploadSerializer(Serializer):
    deals = FileField()
