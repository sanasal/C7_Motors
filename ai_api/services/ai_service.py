from .openai_service import ask_openai
import json
from .data_services import search_cars , finance_car
from .memory_service import save_slug , get_slug

SYSTEM_PROMPT = """
You are a professional sales assistant for C7 Motors.

Your responsibilities:
- Help customers find vehicles.
- Help customers with financing questions.
- Help customers with dealership information.
"""

SEARCH_CARS_TOOL = {
    "type": "function",
    "name": "search_cars",
    "description": """
    Search available cars in C7 Motors inventory.
    Use when customer asks about vehicles,
    prices, availability, brands, models or years.
    """,
    "parameters": {
        "type": "object",
        "properties": {
            "brand": {
                "type": "string"
            },
            "model": {
                "type": "string"
            },
            "year": {
                "type": "integer"
            },
            "exterior_color": {
                "type": "string"
            },
            "body_type": {
                "type": "string"
            },
            "transmission": {
                "type": "string"
            },
            "from_price": {
                "type": "integer"
            },
            "to_price": {
                "type": "integer"
            },
        }
    }
}

FINANCE_CAR_TOOL = {
    "type": "function",
    "name": "finance_car",
    "description": "Calculate financing information",
    "parameters": {
        "type": "object",
        "properties": {
            "downpayment": {
                "type": "float"
            },
            "interest_rate": {
                "type": "float"
            },
            "loan_period": {
                "type": "integer"
            },
        }
    }
}

def process_message(message,visitor_id):

    try:
        response = ask_openai(
            message,
            tools=[SEARCH_CARS_TOOL,
                   FINANCE_CAR_TOOL]
        )

        for item in response.output:

            print("TYPE:", item.type)

            if item.type == "function_call":

                arguments = json.loads(item.arguments)

                if item.name == "search_cars":

                    results = search_cars(
                        brand=arguments.get("brand"),
                        model=arguments.get("model"),
                        year=arguments.get("year"),
                        exterior_color=arguments.get("exterior_color"),
                        body_type=arguments.get("body_type"),
                        transmission=arguments.get("transmission"),
                        from_price=arguments.get("from_price"),
                        to_price=arguments.get("to_price"),
                    )

                    if len(results) == 1:
                        save_slug(visitor_id,results[0]["slug"])
                    


                elif item.name == "finance_car":
                    slug = get_slug(visitor_id)
                    if slug:
                        results = finance_car(
                            car_slug=slug,
                            downpayment=arguments.get("downpayment", 0),
                            interest_rate=arguments.get("interest_rate", 2.79),
                            loan_period=arguments.get("loan_period", 5),
                        )
                    else:
                        results = "Please select a vehicle first."
                    

                tool_prompt = f"""
                You are a professional sales assistant for C7 Motors.

                Customer asked:

                {message}

                Database results:

                {results}

                Answer naturally and professionally.
                """

                final_response = ask_openai(
                    tool_prompt
                )

                print(final_response.output_text)

                return final_response.output_text

    except Exception as e:
        print("ERROR:")
        print(type(e))
        print(e)