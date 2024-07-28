import click
from sqlalchemy import create_engine, MetaData, Table, select, update
from geopy.distance import geodesic
from distance_calculator.google_maps import get_geocode

# Database connection parameters
DB_ENGINE = 'mysql+pymysql'
DB_NAME = 'AccommodationDB'
DB_USER = 'root'
DB_PASSWORD = '98Naturena!!'
DB_HOST = 'localhost'
DB_PORT = '3306'

# UFS campus addresses for geolocation
UFS_CAMPUS_ADDRESSES = {
    'Qwaqwa Campus': 'Kestell Road Qwaqwa, Phuthaditjhaba, 9866',
    'South Campus': 'Oliver Tambo Rd, Ehrlich Park, Bloemfontein, 9301',
    'Bloemfontein Campus': '205 Nelson Mandela Drive Park West Bloemfontein 9301',
}

# Create the engine and session
engine = create_engine(f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
connection = engine.connect()
metadata = MetaData()

# Reflect the existing database table structure
accommodations_table = Table('accommodations', metadata, autoload_with=engine)

def find_nearest_campus(street_address, campuses):
    """
    Find the nearest UFS campus to the given street address.

    Args:
        street_address (str): The address of the accommodation.
        campuses (dict): A dictionary of campus names and their addresses.

    Returns:
        str: The name of the nearest campus or None if not found.
    """
    try:
        # Geocode the accommodation address
        accommodation_location = get_geocode(street_address)
        if not accommodation_location:
            print(f"Could not geocode address: {street_address}")
            return None

        # Extract latitude and longitude from geocoded result
        accommodation_coords = accommodation_location[0].get('geometry', {}).get('location')
        accommodation_latlng = (accommodation_coords['lat'], accommodation_coords['lng'])

        nearest_campus = None
        shortest_distance = float('inf')

        # Calculate distance to each campus and find the nearest one
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
    """
    Update the nearest campus in the database for the given accommodation ID.

    Args:
        accommodation_id (int): The ID of the accommodation to update.
        nearest_campus (str): The name of the nearest campus.

    Returns:
        None
    """
    try:
        # Prepare the SQL update statement
        stmt = (
            update(accommodations_table)
            .where(accommodations_table.c.id == accommodation_id)
            .values(Nearest_Campus=nearest_campus)
        )
        # Execute the update statement
        connection.execute(stmt)
        print(f"Updated Accommodation ID {accommodation_id} with Nearest Campus: {nearest_campus}")
    except Exception as e:
        print(f"Error updating accommodation ID {accommodation_id} in the database: {e}")

def verify_updates():
    """
    Print the results from the database for accommodations associated with UFS.

    Returns:
        None
    """
    try:
        # Query the database for UFS accommodations
        query = select(accommodations_table).where(accommodations_table.c.university == 'UFS')
        results = connection.execute(query).fetchall()
        # Print each accommodation's ID and nearest campus
        for accommodation in results:
            print(f"Accommodation ID {accommodation[0]} - Nearest Campus: {accommodation[6]}")
    except Exception as e:
        print(f"Error verifying updates: {e}")

@click.command()
def update_nearest_campus():
    """
    Update the nearest campus for all UFS accommodations in the database.

    Returns:
        None
    """
    # Query the database for UFS accommodations
    query = select(accommodations_table).where(accommodations_table.c.university == 'UFS')
    results = connection.execute(query).fetchall()

    # Process each accommodation
    for accommodation in results:
        try:
            street_address = accommodation[5]
            nearest_campus = find_nearest_campus(street_address, UFS_CAMPUS_ADDRESSES)
            if nearest_campus:
                # Update the nearest campus in the database
                update_nearest_campus_in_db(accommodation[0], nearest_campus)
            else:
                print(f"Accommodation ID {accommodation[0]} - Could not find nearest campus")

        except Exception as e:
            print(f"Error processing accommodation ID {accommodation[0]}: {e}")

    # Commit the session to save changes
    connection.commit()
    print("Database update complete. Verifying updates...")

    # Print results to verify updates
    verify_updates()

    connection.close()

if __name__ == '__main__':
    update_nearest_campus()
