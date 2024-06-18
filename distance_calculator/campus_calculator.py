import click
from sqlalchemy import create_engine, MetaData, Table, select
from geopy.distance import geodesic
from google_maps import get_geocode  # Assuming google_maps.py is in the same directory

DB_ENGINE = 'mysql+pymysql'
DB_NAME = 'AccommodationDB'
DB_USER = 'root'
DB_PASSWORD = '98Naturena!!'
DB_HOST = 'localhost'
DB_PORT = '3306'

UJ_CAMPUS_ADDRESSES = {
    'Kingsway Campus': 'Kingsway Campus UJ Auckland Park, Rossmore, Johannesburg, 2092',
    'Bunting Road Campus': 'UJ Bunting Road Campus, 37 Bunting Rd, Cottesloe, Johannesburg, 2092',
    'Doornfontein Campus': 'University Of Johannesburg Doornfontein Campus, 55 Beit St, Doornfontein, Johannesburg, 2028',
    'Soweto Campus': 'University of Johannesburg - Soweto Campus, Chris Hani, Soweto, Johannesburg, 1809',
}

engine = create_engine(f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
connection = engine.connect()
metadata = MetaData()
accommodations_table = Table('accommodations', metadata, autoload_with=engine)

def find_nearest_campus(street_address, campuses):
    try:
        accommodation_location = get_geocode(street_address)
        if not accommodation_location:
            return None

        accommodation_coords = accommodation_location[0].get('geometry', {}).get('location')
        accommodation_latlng = (accommodation_coords['lat'], accommodation_coords['lng'])

        nearest_campus = None
        shortest_distance = float('inf')

        for campus_name, campus_address in campuses.items():
            campus_location = get_geocode(campus_address)
            if campus_location:
                campus_coords = campus_location[0].get('geometry', {}).get('location')
                campus_latlng = (campus_coords['lat'], campus_coords['lng'])
                distance = geodesic(accommodation_latlng, campus_latlng).kilometers

                if distance < shortest_distance:
                    shortest_distance = distance
                    nearest_campus = campus_name

        return nearest_campus

    except Exception as e:
        print(f"Error finding nearest campus for {street_address}: {e}")
        return None

@click.command()
def update_nearest_campus():
    query = select(accommodations_table).where(accommodations_table.c.university == 'UJ')
    results = connection.execute(query).fetchall()

    for accommodation in results:
        try:
            street_address = accommodation[3]  # Assuming 'Street_Address' is in position 4 (index 3)
            nearest_campus = find_nearest_campus(street_address, UJ_CAMPUS_ADDRESSES)
            if nearest_campus:
                print(f"Accommodation ID {accommodation[0]} - Nearest campus: {nearest_campus}")
            else:
                print(f"Accommodation ID {accommodation[0]} - Could not find nearest campus")

        except Exception as e:
            print(f"Error processing accommodation ID {accommodation[0]}: {e}")

    connection.close()

if __name__ == '__main__':
    update_nearest_campus()
