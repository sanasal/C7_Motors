#views.py

from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import login , logout
from django.views.decorators.csrf import csrf_protect , csrf_exempt
from . import forms , forms2
from .models import customers_data, Car, CarsCart , Cart , InstallmentsCustomer
from django.http import HttpResponse , JsonResponse , HttpResponseBadRequest
from django.template import Template , Context
import json  
import stripe
from django.conf import settings
from django.views import View
import os
from django.utils import timezone
from django.views.decorators.http import require_http_methods
    
def home(request):
    '''Display the home page'''
    cars = Car.objects.all()
  
    try:
        last_customer_data = customers_data.objects.filter(user=request.user).order_by('-id').first()
        remaining_price = last_customer_data.remaining_amount
    except:
        remaining_price = 0

    try:
        stripe_remaining = remaining_price
    except:
        stripe_remaining = 0

    context = {
        'stripe_remaining': stripe_remaining,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
        'cars': cars,
    }

    return render(request, 'home.html', context)


def contact_us(request):
    '''Display the contact us page'''
    
    try:
        last_customer_data = customers_data.objects.filter(user=request.user).order_by('-id').first()
        remaining_price = last_customer_data.remaining_amount
    except:
        remaining_price = 0

    try:
        stripe_remaining = remaining_price
    except:
        stripe_remaining = 0

    context = {
        'stripe_remaining': stripe_remaining,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request , 'contact_us.html' , context)

def service(request):
    '''Display the services page'''
    try:
        last_customer_data = customers_data.objects.filter(user=request.user).order_by('-id').first()
        remaining_price = last_customer_data.remaining_amount
    except:
        remaining_price = 0

    try:
        stripe_remaining = remaining_price
    except:
        stripe_remaining = 0

    context = {
        'stripe_remaining': stripe_remaining,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request , 'service.html' , context)

def feature(request):
    '''Display the features page'''
    try:
        last_customer_data = customers_data.objects.filter(user=request.user).order_by('-id').first()
        remaining_price = last_customer_data.remaining_amount
    except:
        remaining_price = 0

    try:
        stripe_remaining = remaining_price
    except:
        stripe_remaining = 0

    context = {
        'stripe_remaining': stripe_remaining,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request , 'feature.html' , context)

def about(request):
    '''Display the about page'''
    try:
        last_customer_data = customers_data.objects.filter(user=request.user).order_by('-id').first()
        remaining_price = last_customer_data.remaining_amount
    except:
        remaining_price = 0

    try:
        stripe_remaining = remaining_price
    except:
        stripe_remaining = 0

    context = {
        'stripe_remaining': stripe_remaining,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request , 'about.html' , context)

@login_required(login_url='/log_in/')
def shopping_cart(request):
    '''Display the shopping cart page'''
    cart = None        
    cartitems = []

    if request.user.is_authenticated:
        cart , created = Cart.objects.get_or_create(user =request.user , completed = False)
        cartitems = cart.cartitems.all()

    try:
        stripe_total_price = cart.total_price()  # Assuming the price is in AED
        stripe_deposit = int(3000)
    except:
        stripe_total_price = 0
        stripe_deposit = 0

    context = {
        'cart' : cart , 
        'items':cartitems,
        'stripe_total_price':stripe_total_price,
        'stripe_deposit' : stripe_deposit,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request , 'shopping_cart.html' , context)

def payments_in_installments(request):
    '''Display payment in installments page and save customer data to InstallmentsCustomer model'''
    cart = None        
    cartitems = []

    if request.user.is_authenticated:
        cart , created = Cart.objects.get_or_create(user =request.user , completed = False)
        cartitems = cart.cartitems.all()

    try:
        stripe_deposit = int(3000)
    except:
        stripe_deposit = 0

    context = {
        'cart' : cart , 
        'items':cartitems,
        'stripe_deposit' : stripe_deposit,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request , 'payment_in_installments.html' , context)




def cars_search(request):
    '''get the car from the DataBase'''
    
    # Initialize query parameters
    year = request.GET.get('year')
    brand = request.GET.get('brand')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    # Start with all cars
    cars = Car.objects.all()

    # Apply filters
    if year:
        cars = cars.filter(model_year=year)  # Exact match for year
    if brand:
        cars = cars.filter(brand_name__icontains=brand)  # Case-insensitive partial match for brand
    if price_min and price_max:
        cars = cars.filter(cash_price__gte=int(price_min), cash_price__lte=int(price_max))  # Price range filter

    return render(request, 'home.html', {'cars': cars})

def car_details(request, car_name, car_model, car_id):
    """Display the details of a car based on brand_name, model, and id."""
    try:
        last_customer_data = customers_data.objects.filter(user=request.user).order_by('-id').first()
        remaining_price = last_customer_data.remaining_amount
    except:
        remaining_price = 0

    try:
        stripe_remaining = remaining_price
    except:
        stripe_remaining = 0

    try:
        # Retrieve the car object matching the parameters
        car = Car.objects.get(brand_name=car_name, model=car_model, id=car_id)
    except Car.DoesNotExist:
        # Return a 404 response if the car doesn't exist
        return HttpResponseNotFound("Car not found")
    except Car.MultipleObjectsReturned:
        # Handle cases where multiple cars match the query
        return HttpResponseBadRequest("Multiple cars with the same name and model found")
    except ValueError:
        # Handle invalid `car_id`
        return HttpResponseBadRequest("Invalid ID")

    # Fetch all images related to the car
    car_images = car.images.all()

    description_lines = car.description.splitlines()

    context = {
        'stripe_remaining': stripe_remaining,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
        'description_lines': description_lines,
        'car': car,
        'car_images': car_images,  # Pass images to the template
    }

    return render(request, 'car_details.html', context)





def add_customers_data(request):
    '''Add the customers data to customers_data model'''
    if request.method == 'POST':
        # Determine the payment type (deposit or full)
        payment_type = request.POST.get('payment_type', 'deposit')  # Default to 'deposit'

        form = forms.Customers_Data(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user

            # Get the cart total amount
            cart = Cart.objects.filter(user=request.user, completed=False).first()
            if cart:
                instance.total_amount = cart.total_price()  # Get total price from the cart
            else:
                return JsonResponse({'success': False, 'error': 'Cart not found.'}, status=404)

            if payment_type == 'deposit':
                # Handle deposit payment
                payment_amount = request.POST.get('payment_amount', '3000')  # Default to 3000 if missing
                try:
                    deposit_amount = float(3000)
                    instance.paid_amount = deposit_amount
                    instance.remaining_amount = max(0, instance.total_amount - deposit_amount)
                except ValueError:
                    return JsonResponse({'success': False, 'error': 'Invalid deposit amount.'}, status=400)
            elif payment_type == 'full':
                # Handle full payment
                instance.paid_amount = instance.total_amount  # Paid full amount
                instance.remaining_amount = 0  # No remaining amount

            # Save the instance
            instance.save()

            return JsonResponse({
                'success': True,
                'total_price': instance.total_amount,
                'paid_amount': instance.paid_amount,
                'remaining_amount': instance.remaining_amount
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

def add_payment_data(request):
    '''See if the payment is cash or deposit'''
    if request.method == "POST":
        try:
            payment_type = request.POST.get('payment_type')
            payment_amount = request.POST.get('payment_amount', '0')  # Default to 0 if missing

            try:
                payment_amount = float(payment_amount)  # Convert payment amount to float
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid payment amount.'}, status=400)

            # Get the current user and their customer data
            customer_data = customers_data.objects.filter(user=request.user).first()

            if customer_data:
                if payment_type == 'full':
                    # Full payment scenario
                    customer_data.paid_amount = customer_data.total_amount
                    customer_data.remaining_amount = 0
                elif payment_type == 'deposit':
                    # Deposit payment scenario
                    customer_data.paid_amount += 3000
                    customer_data.remaining_amount = max(0, customer_data.total_amount - customer_data.paid_amount)
                else:
                    return JsonResponse({'success': False, 'error': 'Invalid payment type.'}, status=400)

                # Save the updated customer data
                customer_data.save()

                return JsonResponse({
                    'success': True,
                    'paid_amount': customer_data.paid_amount,
                    'remaining_amount': customer_data.remaining_amount
                })
            else:
                return JsonResponse({'success': False, 'error': 'Customer data not found.'}, status=404)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid payment amount.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

def add_installments_data(request):
    '''Add the customers data whose pay in installments to InstallmentsCustomer model'''
    if request.method == 'POST':

        form = forms2.Installments_Customers_Data(request.POST , request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user

            # Get the cart total amount
            cart = Cart.objects.filter(user=request.user, completed=False).first()
            if cart:
                instance.total_amount = cart.total_price()  # Get total price from the cart
            else:
                return JsonResponse({'success': False, 'error': 'Cart not found.'}, status=404)

            payment_amount = request.POST.get('payment_amount', '3000')  # Default to 3000 if missing
            try:
                deposit_amount = float(3000)
                instance.paid_amount = deposit_amount
                instance.remaining_amount = max(0, instance.total_amount - deposit_amount)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid deposit amount.'}, status=400)

            # Save the instance
            instance.save()

            return JsonResponse({
                'success': True,
                'total_price': instance.total_amount,
                'paid_amount': instance.paid_amount,
                'remaining_amount': instance.remaining_amount
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)




stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt  # You may need to exempt this view from CSRF, or handle it with a middleware
def create_cash_checkout_session(request):
    '''Create Stripe checkout page for cash pay'''
    try:
        # Get the request data
        data = json.loads(request.body)

        cart = None        
        cartitems = []
        
        if request.user.is_authenticated:
            cart , created = Cart.objects.get_or_create(user =request.user , completed = False)
            cartitems = cart.cartitems.all()

        # Calculate the total amount using total_price()
        total_amount = int(cart.total_price() * 100) 
    
        # Create the Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'AED',  # Adjust currency if needed
                        'product_data': {
                            'name': 'C7 Motors',  # The product description shown on Stripe Checkout
                        },
                        'unit_amount': total_amount,  # The amount in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',  # Single full payment mode
                success_url='https://c7motors-cracgggsbcchenap.uaenorth-01.azurewebsites.net/C7_payment_success/',  # Adjust the URL to your success page
                cancel_url='https://c7motors-cracgggsbcchenap.uaenorth-01.azurewebsites.net/cash_cancel/',  # Adjust the URL to your cancel page
        )

        # Return the session ID as JSON response
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def create_deposit_checkout_session(request):
    '''Create Stripe checkout page for deposit pay'''
    try:
        # Get the request data
        data = json.loads(request.body)

        # Calculate the total amount using total_price()
        total_amount = int(3000 * 100)
            
        # Create the Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'AED',  # Adjust currency if needed
                        'product_data': {
                            'name': 'Deposit C7 Motors',  # The product description shown on Stripe Checkout
                        },
                        'unit_amount': total_amount,  # The amount in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',  # Single full payment mode
                success_url='https://c7motors-cracgggsbcchenap.uaenorth-01.azurewebsites.net/C7_payment_success/',  # Adjust the URL to your success page
                cancel_url='https://c7motors-cracgggsbcchenap.uaenorth-01.azurewebsites.net/deposit_cancel/',  # Adjust the URL to your cancel page
        )

        # Return the session ID as JSON response
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def create_remaining_checkout_session(request):
    '''Create Stripe checkout page for remaining price'''
    try:
        try:
            # Get the request data
            last_customer_data = customers_data.objects.filter(user=request.user).order_by('-id').first()
            total_amount = int(last_customer_data.remaining_amount * 100)
        except:
            total_amount = 0

        # Create the Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'AED',  # Adjust currency if needed
                    'product_data': {
                        'name': 'Remaining Price C7 Motors',  # The product description shown on Stripe Checkout
                    },
                    'unit_amount': total_amount,  # The amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',  # Single full payment mode
            success_url='https://c7motors-cracgggsbcchenap.uaenorth-01.azurewebsites.net/C7_remaining_payment_success/',
            cancel_url='https://c7motors-cracgggsbcchenap.uaenorth-01.azurewebsites.net/remaining_cancel/',
        )

        # Return the session ID as JSON response
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def create_installments_checkout_session(request):
    '''Create Stripe checkout page for installments payment pay'''
    try:
        # Get the request data
        data = json.loads(request.body)

        # Calculate the total amount using total_price()
        total_amount = int(3000 * 100)
            
        # Create the Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'AED',  # Adjust currency if needed
                        'product_data': {
                            'name': 'Installments C7 Motors',  # The product description shown on Stripe Checkout
                        },
                        'unit_amount': total_amount,  # The amount in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',  # Single full payment mode
                success_url='https://c7motors-cracgggsbcchenap.uaenorth-01.azurewebsites.net/C7_installments_deposit_payment_success/',  # Adjust the URL to your success page
                cancel_url='https://c7motors-cracgggsbcchenap.uaenorth-01.azurewebsites.net/installments_cancel/',  # Adjust the URL to your cancel page
        )

        # Return the session ID as JSON response
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




def send_book_data_after_success(request):
    '''Send the data to email if the payment is successful and delete the car from the database and customer's cart'''
    customer_book_data = None
    if request.user.is_authenticated:
        customer_book_data = customers_data.objects.filter(user=request.user).order_by('-id').first()
    else:
        print('error')

    context = {
       'customer_book_data': customer_book_data
    }

    return render(request, 'success.html', context)

def remaining_payment_success(request):
    """Handle successful payments and updates customer data."""
    try:
        # Update customer data
        if request.user.is_authenticated:
            last_customer_data = customers_data.objects.filter(user=request.user).order_by('-id').first()
        else:
            print('error')
        
        if not last_customer_data:
            return JsonResponse({'error': 'Customer data not found.'}, status=404)

        last_customer_data.paid_amount += last_customer_data.remaining_amount
        last_customer_data.remaining_amount = 0
        last_customer_data.save()

    
    except Exception as e:
       return JsonResponse({'error': str(e)}, status=500)

    context = {
       'last_customer_data': last_customer_data
    }

    return render(request, 'remaining_success.html', context)

def installments_payment_success(request):
    '''Handle successful payments and updates customer data.'''
    try:
        # Update customer data
        if request.user.is_authenticated:
            last_customer_data = InstallmentsCustomer.objects.filter(user=request.user).order_by('-id').first()
        else:
            print('error')
        
        if not last_customer_data:
            return JsonResponse({'error': 'Customer data not found.'}, status=404)
    
    except Exception as e:
       return JsonResponse({'error': str(e)}, status=500)

    context = {
       'last_customer_data': last_customer_data,
       "last_customer_data": {
            "name": last_customer_data.name,
            "email": last_customer_data.email,
            "mobile_phone": last_customer_data.mobile_phone,
            "cars": last_customer_data.cars,
            "total_amount": last_customer_data.total_amount,
            "paid_amount": last_customer_data.paid_amount,
            "remaining_amount": last_customer_data.remaining_amount,
            "bank": last_customer_data.bank,
            "passport": request.build_absolute_uri(last_customer_data.passport.url) if last_customer_data.passport else '',
            "driver_license": request.build_absolute_uri(last_customer_data.driver_license.url) if last_customer_data.driver_license else '',
            "personal_identification_card": request.build_absolute_uri(last_customer_data.personal_identification_card.url) if last_customer_data.personal_identification_card else '',
            "salary_certificate": request.build_absolute_uri(last_customer_data.salary_certificate.url) if last_customer_data.salary_certificate else '',
            "bank_statement": request.build_absolute_uri(last_customer_data.bank_statement.url) if last_customer_data.bank_statement else '',
            "pick_up_date": last_customer_data.pick_up_date,
            "pick_up_time": last_customer_data.pick_up_time,
            "pick_up_location": last_customer_data.pick_up_location,
        }
    }

    return render(request, 'installments_success.html', context)




def cash_payment_cancel(request):
    '''Display cancel page if the cash payment failed''' 
    cart = None        
    cartitems = []

    if request.user.is_authenticated:
            cart , created = Cart.objects.get_or_create(user =request.user , completed = False)
            cartitems = cart.cartitems.all()
            
    # Calculate the total amount using total_price()
    total_amount = int(cart.total_price() * 100)  # Assuming total_price returns value in dollars

    try:
        stripe_total_price = total_amount # Use total_price() instead of price
    except:
        stripe_total_price = 0

    context = {
        'stripe_total_price': stripe_total_price,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'cash_cancel.html', context)

def deposit_payment_cancel(request):
    '''Display cancel page if the deposit payment failed'''
    # Calculate the total amount using total_price()
    deposit = int(3000 * 100)

    try:
        stripe_deposit = deposit
    except:
        stripe_deposit = 0

    context = {
        'stripe_deposit': stripe_deposit,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'deposit_cancel.html', context)

def remaining_payment_cancel(request):
    '''Display cancel page if the remaining payment failed'''
    # Calculate the total amount using total_price()
    last_customer_data = customers_data.objects.filter(user=request.user).order_by('-id').first()
    remaining_price = last_customer_data.remaining_amount

    try:
        stripe_remaining = remaining_price
    except:
        stripe_remaining = 0

    context = {
        'stripe_remaining': stripe_remaining,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'remaining_cancel.html', context)

def installments_payment_cancel(request):
    '''Display cancel page if the deposit installments payment failed'''
    # Calculate the total amount using total_price()
    deposit = int(3000 * 100)

    try:
        stripe_deposit = deposit
    except:
        stripe_deposit = 0

    context = {
        'stripe_deposit': stripe_deposit,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'installments_cancel.html', context)




@csrf_protect
def sign_in(request):
    '''Sign in the website for new users'''
    if request.method =='POST':   
        form = UserCreationForm(request.POST)
        if form.is_valid(): 
            user = form.save()              
            #log the user in
            login(request , user)           
            return redirect('c7_motors:home')
    else:           
       form = UserCreationForm()     
    return render(request, 'sign in.html' , {'form' : form})

@csrf_protect
def log_in(request):
    '''Log in the website for old users'''
    if request.method == 'POST' :   
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request , user)
            if 'next' in request.POST :
                return redirect(request.POST.get('next'))
            else: 
                return redirect ('c7_motors:home')
    else:
        form = AuthenticationForm()
    return render (request , 'log in.html' , {'form':form})

@csrf_protect
def log_out(request):
    '''Go outside the website'''
    if request.method == 'POST':
        logout(request)   
        return redirect ('c7_motors:home')




def add_to_cart(request):
    '''Add Cars To Customer Shopping Cart'''
    data = json.loads(request.body)
    car_id = data["id"]
    car = Car.objects.get(id = car_id)

    if request.user.is_authenticated:
        cart , created = Cart.objects.get_or_create(user =request.user,completed = False)
        cartitems , created = CarsCart.objects.get_or_create(cart = cart,car = car)
        cartitems.save()

    return JsonResponse('Add Item Done' , safe=False)

def delete_item(request):
    '''Delete Cars From Customer Shopping Cart'''
    data = json.loads(request.body)
    car_id = data['id']
    item = Car.objects.get(id = car_id)
    if request.user.is_authenticated:
        cart = Cart.objects.get(user = request.user , completed = False)
        cart_items = CarsCart.objects.filter(cart=cart , car_id =car_id) 
        cart_items.delete()
    return JsonResponse('Delete Item Done' , safe= False)