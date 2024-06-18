from sqlalchemy import create_engine

DATABASE_URI = 'mysql+pymysql://root:98Naturena!!@localhost/AccommodationDB'
try:
    engine = create_engine(DATABASE_URI)
    connection = engine.connect()
    print("Connection successful")
    connection.close()
except Exception as e:
    print(f"Error: {e}")
