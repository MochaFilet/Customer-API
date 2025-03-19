import mysql.connector

# Database connection parameters
db_host = "127.0.0.1"    # Example: "192.168.1.100"
db_port = 3306           # Default MySQL port
db_user = "richa Deepak"        # Example: "richa"
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
         # 2. Create a view of department salary totals
    cursor.execute("""
        CREATE VIEW department_salary_totals AS
        SELECT department, SUM(salary) AS total_salary
        FROM instructors
        GROUP BY department;
    """)
    print("View 'department_salary_totals' created.")

    # 3. Create a role of student
    cursor.execute("CREATE ROLE student;")
    print("Role 'student' created.")

    # 4. Give select privileges on the view faculty to the role student
    cursor.execute("GRANT SELECT ON faculty TO student;")
    print("SELECT privileges on 'faculty' granted to 'student'.")

    # 5. Create a new user and assign her the role of student
    cursor.execute("CREATE USER 'new_user'@'localhost' IDENTIFIED BY 'new_password';")
    cursor.execute("GRANT student TO 'new_user'@'localhost';")
    print("New user 'new_user' created and assigned role 'student'.")

    # 6. Revoke privileges of the new user
    cursor.execute("REVOKE ALL PRIVILEGES ON *.* FROM 'new_user'@'localhost';")
    print("All privileges revoked for 'new_user'.")

    # 7. Remove the role of student
    cursor.execute("REVOKE student FROM 'new_user'@'localhost';")
    print("Role 'student' revoked from 'new_user'.")

    # 8. Give select privileges on the view faculty to the new user
    cursor.execute("GRANT SELECT ON faculty TO 'new_user'@'localhost';")
    print("SELECT privileges on 'faculty' granted to 'new_user'.")

    # 9. Create table teaches2 with same columns as teaches but with an additional constraint on the semester
    cursor.execute("""
        CREATE TABLE teaches2 AS
        SELECT *, CASE
            WHEN semester IN ('fall', 'winter', 'spring', 'summer') THEN semester
            ELSE NULL
        END AS valid_semester
        FROM teaches;
    """)
    print("Table 'teaches2' created.")

    # 10. Create index on ID column of teaches
    cursor.execute("CREATE INDEX idx_teaches_id ON teaches(ID);")
    print("Index 'idx_teaches_id' created on 'teaches' table.")

    # Timing the query with the index
    import time
    start_time = time.time()
    cursor.execute("SELECT * FROM teaches WHERE ID = 1;")
    end_time = time.time()
    print(f"Query with index took {end_time - start_time:.6f} seconds.")

    # Timing the query without the index
    cursor.execute("DROP INDEX idx_teaches_id ON teaches;")
    start_time = time.time()
    cursor.execute("SELECT * FROM teaches WHERE ID = 1;")
    end_time = time.time()
    print(f"Query without index took {end_time - start_time:.6f} seconds.")

    # 11. Drop the index to free up the space
    cursor.execute("DROP INDEX idx_teaches_id ON teaches;")
    print("Index 'idx_teaches_id' dropped.")
        
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

