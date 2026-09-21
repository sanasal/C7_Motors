from rest_framework import serializers
from c7_app.models import Car

class CarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'