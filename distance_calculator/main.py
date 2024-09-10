from .google_maps import get_geocode, gmaps
from .db import get_accommodations_with_null_campus, update_nearest_campus

CAMPUS_ADDRESSES = {
    'North-West University': {
        'Mafikeng': 'North West University Mahikeng, Mmabatho Unit 5, Mahikeng, 2790',
        'Potchefstroom': 'NWU Potchefstroom Campus Student Centre, 2 Hoffman St, Potchefstroom, 2520',
        'Vanderbijlpark': 'North-West University Vaal Triangle Campus, 1174 Hendrick Van Eck Boulevard, Vanderbijlpark, 1900',
    },
    'UJ': {
        'Kingsway Campus': 'Kingsway Campus UJ Auckland Park, Rossmore, Johannesburg, 2092',
        'Bunting Road Campus': 'UJ Bunting Road Campus, 37 Bunting Rd, Cottesloe, Johannesburg, 2092',
        'Doornfontein Campus': 'University Of Johannesburg Doornfontein Campus, 55 Beit St, Doornfontein, Johannesburg, 2028',
        'Soweto Campus': 'University of Johannesburg - Soweto Campus, Chris Hani, Soweto, Johannesburg, 1809',
    }
}

def calculate_distance_and_time_to_campuses(street_address):
    """
    Calculates the distance and time from the given address to each campus for driving and walking.
    """
    results = {}

    # Get geocode location of the accommodation
    accommodation_location = get_geocode(street_address)
    
    if not accommodation_location:
        return None

    accommodation_coords = accommodation_location[0].get('geometry', {}).get('location')

    for university, campuses in CAMPUS_ADDRESSES.items():
        results[university] = {}
        for campus_name, campus_address in campuses.items():
            # Get geocode location of the campus
            campus_location = get_geocode(campus_address)

            if campus_location:
                campus_coords = campus_location[0].get('geometry', {}).get('location')
                results[university][campus_name] = {}

                for mode in ["driving", "walking"]:
                    distance_result = gmaps.distance_matrix(
                        origins=[accommodation_coords],
                        destinations=[campus_coords],
                        mode=mode
                    )

                    if distance_result['rows'][0]['elements'][0]['status'] == 'OK':
                        distance = distance_result['rows'][0]['elements'][0]['distance']['text']
                        duration = distance_result['rows'][0]['elements'][0]['duration']['text']
                        results[university][campus_name][mode] = {
                            'distance': distance,
                            'duration': duration
                        }

    return results

def determine_nearest_campus(campuses):
    """
    Determines the nearest campus based on the calculated distances and durations.
    """
    nearest_campus = None
    shortest_distance = float('inf')

    for campus_name, campus_info in campuses.items():
        # Assume driving distance is the priority for determining the nearest campus
        if 'driving' in campus_info:
            distance_str = campus_info['driving']['distance']
            distance = float(''.join(filter(str.isdigit, distance_str)))  # Convert distance to number
            
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_campus = campus_name

    return nearest_campus

def update_all_accommodations(university):
    """
    Fetch accommodations with null nearest campus for the given university, calculate distances, 
    determine the nearest campus, and update the database.
    """
    accommodations = get_accommodations_with_null_campus(university)

    for accommodation in accommodations:
        street_address = accommodation['Street_Address']
        results = calculate_distance_and_time_to_campuses(street_address)
        
        if not results:
            continue
        
        nearest_campus = determine_nearest_campus(results.get(university, {}))
        if nearest_campus:
            update_nearest_campus(accommodation['id'], nearest_campus)
        else:
            print(f"Could not determine the nearest campus for Accommodation ID {accommodation['id']}")
