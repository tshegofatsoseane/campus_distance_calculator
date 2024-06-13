import mysql.connector
from .settings import DB_CONFIG

def get_accommodations_with_null_campus(university):
    conn = mysql.connector.connect(
        host=DB_CONFIG['HOST'],
        user=DB_CONFIG['USER'],
        password=DB_CONFIG['PASSWORD'],
        database=DB_CONFIG['NAME'],
        port=DB_CONFIG['PORT']
    )
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT id, Street_Address
    FROM accommodations_accommodation
    WHERE Nearest_Campus IS NULL
    AND university = %s
    """
    cursor.execute(query, (university,))
    results = cursor.fetchall()
    conn.close()
    return results

def update_nearest_campus(accommodation_id, nearest_campus):
    conn = mysql.connector.connect(
        host=DB_CONFIG['HOST'],
        user=DB_CONFIG['USER'],
        password=DB_CONFIG['PASSWORD'],
        database=DB_CONFIG['NAME'],
        port=DB_CONFIG['PORT']
    )
    cursor = conn.cursor()
    update_query = """
    UPDATE accommodations_accommodation
    SET Nearest_Campus = %s
    WHERE id = %s
    """
    cursor.execute(update_query, (nearest_campus, accommodation_id))
    conn.commit()
    conn.close()