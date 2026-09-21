from rest_framework import generics
from c7_app.models import Car
from .serializer import CarsSerializer

class CarsAPI(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarsSerializer