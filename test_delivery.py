from backend.database import DB_connection
import random

conn = DB_connection()
cur = conn.cursor()

# Test the exact query
cur.execute("SELECT id FROM users WHERE role = 'delivery_person'")
delivery_personnel = cur.fetchall()

print("Delivery personnel found:", delivery_personnel)
print("Type:", type(delivery_personnel))
if delivery_personnel:
    print("First item:", delivery_personnel[0])
    print("First item type:", type(delivery_personnel[0]))
    print("Trying to access 'id':", delivery_personnel[0].get('id') if hasattr(delivery_personnel[0], 'get') else delivery_personnel[0])
    
    # Test random selection
    selected = random.choice(delivery_personnel)
    print("Selected person:", selected)
    if hasattr(selected, 'get'):
        print("Selected ID:", selected.get('id'))
    else:
        print("Selected (tuple):", selected)
else:
    print("No delivery personnel found!")

conn.close()
