from django.contrib import admin
from .models import  Car,Cart , customers_data , CarsCart , CarImages

# Register your models here.
admin.site.register(Car)
admin.site.register(Cart)
admin.site.register(customers_data)
admin.site.register(CarsCart)
admin.site.register(CarImages)