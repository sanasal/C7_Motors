from django import views
from django.urls import path 
from . import views      
from .views import CarDetails,HomeView,InventoryView

app_name='c7_motors'

urlpatterns = [          
    path('lang/<str:lang_code>/', views.switch_language, name='switch_language'),
    
    path('' ,HomeView.as_view(), name='home'),  
    path('about/' , views.about ,name='about'),
    path('inventory/' , InventoryView.as_view() , name='inventory'),
    path('financing/', views.financing, name='financing'),
    path('financing/<slug:car_slug>/', views.financing, name='financing_with_car'),
    path('articles/' , views.articles , name='articles'),
    path('contact_us/' , views.contact_us , name='contact_us'),

    path('car_details/<slug:car_slug>/' , views.car_details, name='car_details'),

    path('add_financig_data/' , views.add_financing_request_data , name = 'add_f_request_data'),
]
