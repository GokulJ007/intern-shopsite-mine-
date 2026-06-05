import pymysql
import pymysql.cursors
from database import DB_connection
from auth import hash_password

def migrate_passwords():
    try:
        connection = DB_connection()
        print("Connected to MySQL database successfully!")
        
        with connection.cursor() as cursor:
            # Get all users with password
            cursor.execute("SELECT id, name, password FROM users")
            users = cursor.fetchall()
            
            updated_count = 0
            for user in users:
                user_id = user['id']
                username = user['name']
                raw_password = user.get('password')
                
                # Check if password is NULL or already looks like a bcrypt hash (e.g. starts with $2b$ or $2a$)
                if not raw_password:
                    print(f"User '{username}' (ID: {user_id}) has no password set. Seeding default '1234' hashed...")
                    hashed = hash_password("1234")
                    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed, user_id))
                    updated_count += 1
                elif not (raw_password.startswith("$2b$") or raw_password.startswith("$2a$")) or len(raw_password) < 50:
                    print(f"Hashing password for user '{username}' (ID: {user_id})...")
                    hashed = hash_password(raw_password)
                    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed, user_id))
                    updated_count += 1
                else:
                    print(f"User '{username}' (ID: {user_id}) already has a hashed password.")
            
            connection.commit()
            print(f"\nMigration completed! Hashed and updated {updated_count} user passwords.")
            
    except Exception as e:
        print("Failed to run password migration:", e)
    finally:
        if 'connection' in locals() and connection:
            connection.close()

if __name__ == "__main__":
    migrate_passwords()
