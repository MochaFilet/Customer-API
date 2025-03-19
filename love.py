import mysql.connector

# Database connection parameters
db_host = "127.0.0.1"    # Example: "192.168.1.100"
db_port = 3306           # Default MySQL port
db_user = "richa"        # Example: "richa"
db_password = "richDeep" # Your database password
db_name = "FARHAN"       # The database you want to connect to

try:
    # Establish connection to MySQL database
    conn = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name
    )

    # Check if connection is successful
    if conn.is_connected():
        print(f"Connected to MySQL database at {db_host}:{db_port}")
        
        # Create cursor
        cursor = conn.cursor()
        
        # Execute SELECT query
        cursor.execute("SELECT * FROM kids;")
        
        # Fetch and print results
        rows = cursor.fetchall()
        for row in rows:
            print(row)

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()  # Close cursor
        conn.close()    # Close connection
        print("Database connection closed.")

