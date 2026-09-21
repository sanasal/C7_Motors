from c7_app.models import Car
from django.db.models import Q


def search_cars(brand=None,model=None,year=None,exterior_color=None,body_type=None,transmission=None,from_price=0,to_price=900000):
    
    results = []

    cars = Car.objects.filter(Q(selled=False) & Q(not_available=False))
    
    if brand:
        cars = cars.filter(brand_name__iexact=brand)
    
    if model:
        cars = cars.filter(model__iexact=model)

    if year:
        cars = cars.filter(model_year=year)

    if exterior_color:
        cars = cars.filter(exterior_color__icontains=exterior_color)

    if body_type:
        cars = cars.filter(type__icontains=body_type)

    if transmission:
        cars = cars.filter(transmission__icontains=transmission)

    if from_price and to_price:
        cars = cars.filter(cash_price__range=(from_price,to_price))


    for car in cars:
        results.append(
            {
                "slug": car.slug,
                "brand": car.brand_name,
                "model": car.model,
                "year": car.model_year,
                "price": car.cash_price,
            }
        )

    return results



def finance_car(
    car_slug,
    downpayment=0,
    interest_rate=2.79,
    loan_period=5
):

    car = Car.objects.get(
        slug=car_slug
    )

    price = float(car.cash_price)

    loan_amount = price - downpayment

    total_interest = (
        loan_amount *
        (interest_rate / 100) *
        loan_period
    )

    total_price = (
        loan_amount +
        total_interest
    )

    monthly_payment = (
        total_price /
        (loan_period * 12)
    )

    return {
        "monthly_payment": round(monthly_payment, 2),
        "downpayment": downpayment,
        "loan_amount": round(loan_amount, 2),
        "total_interest": round(total_interest, 2),
        "total_price": round(total_price, 2),
        "loan_period_years": loan_period,
    }