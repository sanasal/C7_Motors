from django.urls import path
from .views import CarsAPI

app_name = 'ai_api'

urlpatterns = [ 
   path('',CarsAPI.as_view(),name='cars_model_ser'),
]
