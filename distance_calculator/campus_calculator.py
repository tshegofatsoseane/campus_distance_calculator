import click
from sqlalchemy import create_engine, MetaData, Table, select, update
from geopy.distance import geodesic
from google_maps import get_geocode  

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
            print(f"Could not geocode address: {street_address}")
            return None

        accommodation_coords = accommodation_location[0].get('geometry', {}).get('location')
        accommodation_latlng = (accommodation_coords['lat'], accommodation_coords['lng'])

        nearest_campus = None
        shortest_distance = float('inf')

        for campus_name, campus_address in campuses.items():
            campus_location = get_geocode(campus_address)
            if not campus_location:
                print(f"Could not geocode campus address: {campus_address}")
                continue

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

def update_nearest_campus_in_db(accommodation_id, nearest_campus):
    try:
        stmt = update(accommodations_table).where(accommodations_table.c.id == accommodation_id).values(Nearest_Campus=nearest_campus)
        connection.execute(stmt)
        print(f"Updated Accommodation ID {accommodation_id} with Nearest Campus: {nearest_campus}")
    except Exception as e:
        print(f"Error updating accommodation ID {accommodation_id} in the database: {e}")

def verify_updates():
    try:
        query = select(accommodations_table).where(accommodations_table.c.university == 'UJ')
        results = connection.execute(query).fetchall()
        for accommodation in results:
            print(f"Accommodation ID {accommodation[0]} - Nearest Campus: {accommodation[6]}")
    except Exception as e:
        print(f"Error verifying updates: {e}")

@click.command()
def update_nearest_campus():
    query = select(accommodations_table).where(accommodations_table.c.university == 'UJ')
    results = connection.execute(query).fetchall()

    for accommodation in results:
        try:
            street_address = accommodation[5]
            nearest_campus = find_nearest_campus(street_address, UJ_CAMPUS_ADDRESSES)
            if nearest_campus:
                update_nearest_campus_in_db(accommodation[0], nearest_campus)
            else:
                print(f"Accommodation ID {accommodation[0]} - Could not find nearest campus")

        except Exception as e:
            print(f"Error processing accommodation ID {accommodation[0]}: {e}")

    verify_updates()
    connection.close()

if __name__ == '__main__':
    update_nearest_campus()
