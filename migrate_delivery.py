import os
import pymysql
from dotenv import load_dotenv

def migrate():
    # Load environment variables from backend/.env
    load_dotenv('backend/.env')
    
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'defaultdb')
    port = int(os.getenv('DB_PORT', 3306))
    
    ssl_config = {'ssl_mode': 'REQUIRED'} if 'aivencloud.com' in host else None
    
    print(f"Connecting to database {database} on {host}:{port}...")
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            ssl=ssl_config
        )
        print("Connected to MySQL database successfully!")
        
        with connection.cursor() as cursor:
            # Check if columns already exist
            cursor.execute("DESCRIBE orders")
            columns = cursor.fetchall()
            column_names = [col[0] for col in columns]
            
            # Add delivery_status if it doesn't exist
            if 'delivery_status' not in column_names:
                print("Adding 'delivery_status' column to 'orders' table...")
                cursor.execute("ALTER TABLE orders ADD COLUMN delivery_status VARCHAR(50) DEFAULT 'Pending'")
                print("Column 'delivery_status' added successfully!")
            else:
                print("'delivery_status' column already exists in 'orders' table.")
                
            # Add delivery_person_id if it doesn't exist
            if 'delivery_person_id' not in column_names:
                print("Adding 'delivery_person_id' column to 'orders' table...")
                cursor.execute("ALTER TABLE orders ADD COLUMN delivery_person_id INT DEFAULT NULL")
                print("Column 'delivery_person_id' added successfully!")
            else:
                print("'delivery_person_id' column already exists in 'orders' table.")
                
            connection.commit()
            print("Database migration completed successfully!")
            
    except Exception as e:
        print("Migration failed:", e)
    finally:
        if 'connection' in locals() and connection:
            connection.close()

if __name__ == "__main__":
    migrate()
