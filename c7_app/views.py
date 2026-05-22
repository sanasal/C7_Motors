# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils import translation
from django.views.decorators.http import require_http_methods 
from django.http import JsonResponse
import json, urllib
from .models import Car, Article
from .forms import RequestsForm
from c7_motors import deployment
from django.views.generic import ListView , DetailView
from django.db.models import Q


def switch_language(request, lang_code):
    translation.activate(lang_code)
    request.session['django_language'] = lang_code

    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie(deployment.LANGUAGE_COOKIE_NAME, lang_code)
    return response

class HomeView(ListView):

    model = Car
    template_name = 'home.html'
    context_object_name = 'cars'

    def get_queryset(self):

        car_type = self.request.GET.get('type')

        cars = (
            Car.objects
            .filter(
                selled=False,
                not_available=False
            )
        )

        if car_type:
            cars = cars.filter(type=car_type)

        return (
            cars
            .only(
                'id',
                'cash_price',
                'main_img',
                'brand_name',
                'model',
                'model_year',
                'mileage',
                'transmission',
                'type',
                'slug',
                'selled',
                'not_available'
            )
            .order_by('-id')[:3]
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['articles'] = (
            Article.objects
            .only('id', 'title', 'image')[:4]
        )

        # FIXED
        context['type_choices'] = Car.TYPE_CHOICES

        context['models_years'] = (
            Car.objects
            .values_list(
                'model_year',
                flat=True
            )
            .distinct()
            .order_by('model_year')
        )

        context['cars_brands'] = (
            Car.objects
            .values_list(
                'brand_name',
                flat=True
            )
            .distinct()
            .order_by('brand_name')
        )

        return context



class InventoryView(ListView):
    model = Car
    template_name = 'inventory.html'
    context_object_name = 'cars'

    def get_queryset(self):

        cars = (
            Car.objects
            .only(
                'id',
                'cash_price',
                'main_img',
                'brand_name',
                'model',
                'model_year',
                'mileage',
                'transmission',
                'type',
                'slug',
                'selled',
                'not_available'
            )
            .order_by('-id')
        )

        # FILTERS

        brand = self.request.GET.get('brand')
        model = self.request.GET.get('model')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        year = self.request.GET.get('year')
        body_style = self.request.GET.get('body_style')

        if brand:
            cars = cars.filter(
                brand_name=brand
            )

        if model:
            cars = cars.filter(
                model=model
            )

        if min_price:
            cars = cars.filter(
                cash_price__gte=min_price
            )

        if max_price:
            cars = cars.filter(
                cash_price__lte=max_price
            )

        if year:
            cars = cars.filter(
                model_year=year
            )

        if body_style:
            cars = cars.filter(
                type=body_style
            )

        return cars

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # BRANDS

        context['brands'] = (
            Car.objects
            .values_list(
                'brand_name',
                flat=True
            )
            .distinct()
            .order_by('brand_name')
        )

        # MODELS

        context['models'] = (
            Car.objects
            .values_list(
                'model',
                flat=True
            )
            .distinct()
            .order_by('model')
        )

        # YEARS

        context['years'] = (
            Car.objects
            .values_list(
                'model_year',
                flat=True
            )
            .distinct()
            .order_by('-model_year')
        )

        # BODY STYLES

        context['type_choices'] = (
            Car.TYPE_CHOICES
        )

        return context



def contact_us(request):
    '''Display the contact us page'''

    return render(request , 'contact_us.html')


def about(request):
    '''Display the about page'''

    return render(request , 'about.html')


def articles(request):
    "Display the articles in the articles page"
    articles = Article.objects.all()

    context = {
        'articles' : articles
    }

    return render(request , 'articles.html' , context)


@require_http_methods(["GET", "POST"])
def financing(request , car_slug = None):
    car_price = None

    if car_slug:
        car_price = Car.objects.values_list('ramadan_price', flat=True).get(slug=car_slug)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if car_slug:
                car_price = Car.objects.values_list('ramadan_price', flat=True).get(slug=car_slug)
            else:  
                car_price = float(data.get('car_price', 0))
            downpayment = float(data.get('downpayment', 0))
            loan_duration = int(data.get('loan_duration', 1))

            interest = (car_price * 0.04) / 12
            total = car_price + (interest * loan_duration)
            monthly = (total - downpayment) / loan_duration

            return JsonResponse({
                'estimated_monthly_payment': f"AED {monthly:.2f}"
            })

        except Exception:
            return JsonResponse({'error': 'Invalid data'}, status=400)

    return render(
        request,
        "financing.html",
        {
            'cars': Car.objects.only('id', 'brand_name', 'model'),
            'car_price' : car_price,
            'form': RequestsForm()
        }
    )


def _handle_request_form(request, template):
    form = RequestsForm(request.POST)
    if not form.is_valid():
        return render(request, template, {'form': form})

    data = form.save()

    message = urllib.parse.quote(
        f"Car: {data.car}\n"
        f"Name: {data.name}\n"
        f"Phone: {data.mobile_phone}\n"
        f"Payment: {data.payment_method}\n"
        f"Lang: {data.language}"
    )

    return redirect(f"https://wa.me/971562341000?text={message}")

@require_http_methods(["POST"])
def add_financing_request_data(request):
    return _handle_request_form(request, 'financing.html')



def car_details(request, car_slug):
    car = get_object_or_404(
        Car.objects.prefetch_related(
            'images',
            'technical_features',
            'driver_assistance_and_safty',
            'comfort_and_convenience',
            'exterior'
        ),
        slug=car_slug
    )

    context = {
        'car': car,
        'description_lines': car.description.splitlines(),
        'car_images': car.images.all(),
        'technical_features': car.technical_features.all(),
        'driver_assistance_and_safty': car.driver_assistance_and_safty.all(),
        'comfort_and_convenience': car.comfort_and_convenience.all(),
        'exterior': car.exterior.all(),
    }

    return render(request, 'car_details.html', context)


class CarDetails(DetailView):
    model = Car
    template_name = 'car_details.html'
    context_object_name = 'car'
    slug_field = 'slug'
    slug_url_kwarg = 'car_slug'

    def get_queryset(self):
        return Car.objects.prefetch_related(
            'images',
            'technical_features',
            'driver_assistance_and_safty',
            'comfort_and_convenience',
            'exterior'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.object 

        context.update({
            'description_lines': car.description.splitlines(),
            'car_images': car.images.all(),
            'technical_features': car.technical_features.all(),
            'driver_assistance_and_safty': car.driver_assistance_and_safty.all(),
            'comfort_and_convenience': car.comfort_and_convenience.all(),
            'exterior': car.exterior.all(),
        })