import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os
from contextlib import contextmanager

# .env dosyasını yükle
load_dotenv()

# DB_CONFIG artık .env'den okuyor
DB_CONFIG = {

    "host": os.getenv("DB_HOST"), 
    "user": os.getenv("DB_USER"),           
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306)),  # Varsayılan port 3306
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci"
}

def connect_to_database():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("✅ Successfully connected to the database!")
            return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("❌ ERROR: Username or password is incorrect!")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("❌ ERROR: Database not found!")
        else:
            print(f"❌ ERROR: {err}")
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
    return None

# Test
# print("Trying to connect...")
# conn = connect_to_database()
# if conn:
#     conn.close()
#     print("The connection was closed.")