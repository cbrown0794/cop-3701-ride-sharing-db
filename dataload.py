# dataload.py
import sqlite3
import csv
import os

DB_NAME = 'ride_sharing.db'

def setup_database(cursor):
    print("Creating database schema...")
    with open('create_db.sql', 'r') as f:
        sql_script = f.read()
    cursor.executescript(sql_script)

def load_csv_to_table(cursor, table_name, csv_filename):
    filepath = os.path.join('data', csv_filename)
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        columns = next(reader) # Get headers
        
        # Create dynamic SQL insert query
        placeholders = ','.join(['?' for _ in columns])
        insert_query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
        
        # Insert data
        data = [row for row in reader]
        cursor.executemany(insert_query, data)
        print(f"Loaded {len(data)} records into {table_name}")

def main():
    # Connect to SQLite database (this creates the file if it doesn't exist)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # 1. Run the DDL script
        setup_database(cursor)

        # 2. Load data into tables (Order matters due to Foreign Keys!)
        tables_and_files = [
            ('DISPATCH_BASE', 'dispatch_base.csv'),
            ('VEHICLE', 'vehicle.csv'),
            ('TELEMATICS_TRACKER', 'telematics_tracker.csv'),
            ('ZONE', 'zone.csv'),
            ('SURGE_PERIOD', 'surge_period.csv'),
            ('TRIP', 'trip.csv')
        ]

        for table, filename in tables_and_files:
            load_csv_to_table(cursor, table, filename)

        # Commit changes
        conn.commit()
        print("\nDatabase successfully populated!")

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    main()