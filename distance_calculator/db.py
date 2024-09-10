from sqlalchemy import create_engine, MetaData, Table, select

# Database connection parameters
DB_ENGINE = 'mysql+pymysql'
DB_NAME = 'AccommodationDB'
DB_USER = 'root'
DB_PASSWORD = '98Naturena!!'
DB_HOST = 'localhost'
DB_PORT = '3306'

# Create the engine and metadata
engine = create_engine(f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
metadata = MetaData()
accommodations_table = Table('accommodations', metadata, autoload_with=engine)

def get_accommodations_with_null_campus(university):
    """
    Fetch accommodations with null nearest campus for a specific university.
    
    Args:
        university (str): The university to filter accommodations by.
    
    Returns:
        List[Dict]: List of accommodations with a null nearest campus.
    """
    with engine.connect() as connection:
        query = select(accommodations_table).where(
            accommodations_table.c.university == university,
            accommodations_table.c.Nearest_Campus.is_(None)
        )
        results = connection.execute(query).fetchall()
        # Convert result to a list of dictionaries
        accommodations = [dict(row) for row in results]
    
    return accommodations

def update_nearest_campus(accommodation_id, nearest_campus):
    """
    Update the nearest campus in the database for the given accommodation ID.

    Args:
        accommodation_id (int): The ID of the accommodation to update.
        nearest_campus (str): The name of the nearest campus.
    """
    with engine.connect() as connection:
        stmt = (
            update(accommodations_table)
            .where(accommodations_table.c.id == accommodation_id)
            .values(Nearest_Campus=nearest_campus)
        )
        connection.execute(stmt)
        print(f"Updated Accommodation ID {accommodation_id} with Nearest Campus: {nearest_campus}")
