import sqlite3

# Establish a connection to the database
conn = sqlite3.connect("sample.db")
cursor = conn.cursor()

# Create a table
cursor.execute(
    """
    CREATE TABLE samples (
        id INTEGER PRIMARY KEY,
        city TEXT,
        count INTEGER
    )
    """
)

# Insert sample data
data = [
    ("New York", 100),
    ("London", 75),
    ("Tokyo", 120),
    ("Paris", 50),
    ("Sydney", 90),
]

cursor.executemany("INSERT INTO samples (city, count) VALUES (?, ?)", data)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Sample database created successfully.")
