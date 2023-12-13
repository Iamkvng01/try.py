#code to clear your database

import sqlite3

def clear_database():
    conn = sqlite3.connect('data1.db')
    c = conn.cursor()

    # Execute an SQL query to delete all records from the table
    c.execute('DELETE FROM userstable')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Call the function to clear the database
clear_database()
