import sqlite3

def create_and_populate_database(db_name='large_data.db', num_records=100000):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            value REAL
        )
    ''')

    # Populate with dummy data
    print(f"Populating database with {num_records} records...")
    for i in range(num_records):
        cursor.execute("INSERT INTO sensor_readings (value) VALUES (?)", (i * 0.1 + 20.0,))
    conn.commit()
    print("Database populated.")
    return conn

def process_data_without_cursor(conn):
    print("\nProcessing data WITHOUT cursor (loading all into memory)...\n")
    cursor = conn.cursor()
    cursor.execute("SELECT id, value FROM sensor_readings")
    all_rows = cursor.fetchall() # Loads ALL data into memory
    print(f"Fetched {len(all_rows)} rows. First 5: {all_rows[:5]}")
    # Simulate some processing
    total_value = sum(row[1] for row in all_rows)
    print(f"Simulated processing: Total value = {total_value:.2f}")

def process_data_with_cursor(conn):
    print("\nProcessing data WITH cursor (fetching row by row)...\n")
    cursor = conn.cursor()
    # Declare the cursor as a server-side cursor (if supported, sqlite3 uses it by default for fetchall/fetchmany)
    # For demonstration, we'll simulate fetching one by one
    cursor.execute("SELECT id, value FROM sensor_readings")

    count = 0
    total_value = 0.0
    # Fetch rows one by one to simulate cursor behavior without loading all into memory
    while True:
        row = cursor.fetchone() # Fetches one row at a time
        if row is None:
            break
        count += 1
        total_value += row[1]
        if count <= 5 or count % 10000 == 0: # Print first few and some progress markers
            print(f"Fetched row {count}: ID={row[0]}, Value={row[1]:.2f}")

    print(f"\nFetched {count} rows using fetchone().")
    print(f"Simulated processing: Total value = {total_value:.2f}")

if __name__ == "__main__":
    # Create a database with a large number of records
    connection = create_and_populate_database(num_records=50000) # Reduced for quicker demo

    # Demonstrate processing without a cursor (loads all into memory)
    process_data_without_cursor(connection)

    # Demonstrate processing with a cursor (fetches row by row)
    process_data_with_cursor(connection)

    connection.close()
    print("\nDatabase connection closed.")
