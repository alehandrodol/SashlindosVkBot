import psycopg2

# Connect to the database
conn = psycopg2.connect(
    host="rc1b-yg488vnhrlssml6z.mdb.yandexcloud.net",
    database="db1",
    user="user1",
    password="Tozafa_alex02",
    port="6432"
)

# Open a cursor
cur = conn.cursor()

# Get a list of all sequences in the database
cur.execute("""
    SELECT column_default, table_name, column_name
    FROM information_schema.columns
    WHERE column_default LIKE 'nextval%'
""")
sequences = cur.fetchall()

# Loop through each sequence and refresh its value
for seq in sequences:
    seq_name = seq[0].split("'")[1]
    table_name = seq[1]
    col_name = seq[2]

    # Get the maximum ID value for the associated table
    cur.execute(f"SELECT MAX({col_name}) FROM {table_name}")
    max_id = cur.fetchone()[0]

    # Refresh the sequence's value to the maximum ID value
    cur.execute(f"SELECT setval('{seq_name}', {max_id})")

# Commit the changes and close the connection
conn.commit()
conn.close()
