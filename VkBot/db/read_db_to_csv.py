import psycopg2
import csv

# Establish a connection to the database
conn = psycopg2.connect(
    host="top2.nearest.of.pdr-bot-db.internal",
    database="pdr_bot",
    user="pdr_bot",
    password="F6HlKBoeGf9U2Fg",
    port="5432"
)
# Open a cursor to perform database operations
cur = conn.cursor()

# Retrieve the list of tables from the database
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")

# Fetch all the table names
tables = cur.fetchall()

# Loop through each table and execute a SELECT query
for table in tables:
    # Define the SQL query to select all data from the table
    query = f"SELECT * FROM {table[0]};"

    # Execute the query
    cur.execute(query)

    # Fetch all the results
    results = cur.fetchall()

    # Define the path and filename for the CSV file
    filename = f"./csv/{table[0]}.csv"

    # Write the results to the CSV file
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        # Write the column headers first
        writer.writerow([desc[0] for desc in cur.description])
        # Write the data rows
        for row in results:
            writer.writerow(row)

# Close the cursor and connection
cur.close()
conn.close()
