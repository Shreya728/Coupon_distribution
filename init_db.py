import sqlite3
import os

# Initialize the database
def init_db():
    # Remove existing database if it exists
    if os.path.exists('database.db'):
        os.remove('database.db')
    
    # Create a new database
    conn = sqlite3.connect('database.db')
    
    # Read schema from file
    with open('/Users/shreyaaa/Desktop/coupon_system/schema.sql') as f:
        conn.executescript(f.read())
    
    # Add default admin user
    conn.execute(
        'INSERT INTO admins (username, password) VALUES (?, ?)',
        ('Shreya', 'Shreya123')  # In production, use hashed passwords
    )
    
    # Add some sample coupons
    sample_coupons = [
        'SAVE10NOW',
        'WELCOME20',
        'DISCOUNT30',
        'SPECIAL25',
        'FREESHIP'
    ]
    
    for coupon in sample_coupons:
        conn.execute(
            'INSERT INTO coupons (code, is_active) VALUES (?, 1)',
            (coupon,)
        )
    
    conn.commit()
    conn.close()
    
    print("Database initialized with sample data")

if __name__ == '__main__':
    init_db()
