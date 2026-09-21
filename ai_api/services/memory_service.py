memory = {}


def save_slug(visitor_id,car_slug):
    memory[visitor_id] = {"selected_car_slug": car_slug}
    

def get_slug(visitor_id):
    try:
        slug = memory[visitor_id]["selected_car_slug"]

        if slug:
            return slug
        else:
            return None
        
    except KeyError:
        print("there isn't any visitor that have this id")