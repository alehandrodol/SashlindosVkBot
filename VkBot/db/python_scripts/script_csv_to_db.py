import psycopg2
import csv
import os

# Establish a connection to the database
conn = psycopg2.connect(
    host="rc1b-yg488vnhrlssml6z.mdb.yandexcloud.net",
    database="db1",
    user="user1",
    password="Tozafa_alex02",
    port="6432"
)

# Open a cursor to perform database operations
cur = conn.cursor()

def convert_tuple_to_ints(tup):
    # Convert each element in the tuple to an integer if it's a numeric string
    return tuple(int(x) if x.isnumeric() else x for x in tup)

# Define a function to read a CSV file and insert the data into a database table
def insert_csv_to_db(filename):
    # Extract the table name from the filename (without the ".csv" extension)
    table_name = (os.path.splitext(filename)[0]).split('/')[-1]

    # Open the CSV file and read its contents
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        rows = [convert_tuple_to_ints(tuple(row)) for row in reader]
    
    # Define the SQL query to create a table and insert the data
    insert_query = f"INSERT INTO {table_name} ({', '.join(rows[0])}) VALUES ("
    rows = rows[1:]
    for i, col in enumerate(rows[0]):
        # Add a placeholder to the INSERT query
        insert_query += "%s"
        if i < len(rows[0]) - 1:
            insert_query += ", "
    insert_query += ");"
    
    print(insert_query)
    print(rows)
    # Insert the data into the table
    cur.executemany(insert_query, rows)
    conn.commit()

# Loop through all CSV files in the current directory and insert their data into tables
for filename in os.listdir("./csv"):
    if filename.endswith("votes.csv"):
        insert_csv_to_db("./csv/" + filename)

# Close the cursor and connection
cur.close()
conn.close()

