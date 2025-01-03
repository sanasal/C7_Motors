#models.py
from django.db import models
from xml.parsers.expat import model
from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here

class customers_data(models.Model):
    user = models.ForeignKey(User,null = True, on_delete = models.SET_NULL) 
    cars = models.TextField(default='', blank=True)
    name = models.TextField(max_length=300, default='', blank=True)
    email = models.TextField(max_length=300, default='', blank=True)
    mobile_phone = models.TextField(blank=True, default='')
    total_amount =models.IntegerField(null=True)
    paid_amount = models.IntegerField(null=True)
    remaining_amount = models.IntegerField(null=True , default=0)
    pick_up_location = models.TextField(max_length=300, default='', blank=True)
    pick_up_date = models.DateField(null=True, blank=True)
    pick_up_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True , null=True)

    def save(self, *args, **kwargs):
        # Automatically calculate the remaining amount
        if self.total_amount is not None and self.paid_amount is not None:
            self.remaining_amount = self.total_amount - self.paid_amount
        super(customers_data, self).save(*args, **kwargs)

    def __str__(self):
        return f"cars:{self.cars} - user:{self.user} - name:{self.name}"


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4 , primary_key=True)
    user = models.ForeignKey(User,null = True, on_delete = models.SET_NULL) 
    completed =  models.BooleanField(default=False)

    def total_price(self):

        cartitems = self.cartitems.all()

        cars_total = sum ([item.cars_cash_price() for item in cartitems])

        total_price_without_discount =  cars_total

        total_dicount = 0

        discount = 0

        total_price_after_discount = total_price_without_discount - (total_price_without_discount * discount)

        return int(total_price_after_discount)

    def __str__(self):
       return f"{self.id} - {self.user}"

class Car(models.Model):
    brand_name = models.CharField(max_length=100 , blank=True)
    model = models.CharField(max_length=100 , blank=True)
    main_img = models.ImageField(default = '' , blank=True)
    exterior_color = models.CharField(max_length=100 , blank=True)
    interior_color = models.CharField(max_length=100 , blank=True)
    
    MANUAL = 'Manual'
    AUTOMATIC = 'Automatic'
    GEAR_CHOICES = [
        (MANUAL, 'Manual Transmission'),
        (AUTOMATIC, 'Automatic Transmission'),
    ]
    
    transmission = models.CharField(max_length=20, choices=GEAR_CHOICES)
    model_year = models.IntegerField(null=True, blank=True)
    mileage = models.IntegerField(null=True, blank=True)
    cash_price =models.IntegerField(null=True, blank=True)
    monthly_installments_price = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.brand_name} {self.model}"


class CarImages(models.Model):
    product = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='C7_Motors\media')


class CarsCart(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE , related_name='items')
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE , related_name='cartitems')

    def __str__(self):
        return f"{self.car.brand_name} - ${self.car.cash_price}"

    def cars_cash_price(self):
        car_price = int(self.car.cash_price)
        cars_total_price = car_price
        return cars_total_price