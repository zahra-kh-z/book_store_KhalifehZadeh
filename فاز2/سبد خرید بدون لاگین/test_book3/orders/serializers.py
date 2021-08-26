from rest_framework import serializers
from .models import *


# https://howtojsonapi.com/django.html
class TaskSerializer(serializers.ModelSerializer):
    """convert data app to json"""

    class Meta:
        model = Invoice
        fields = '__all__'
