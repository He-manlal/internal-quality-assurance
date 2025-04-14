import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def delete_process(process_id: int):
    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Execute the DELETE query
        cur.execute("DELETE FROM processes WHERE process_id = %s;", (process_id,))

        # Commit the transaction
        conn.commit()

        # Check if any rows were deleted
        if cur.rowcount == 0:
            raise Exception(f"No process found with the id '{process_id}'.")
        else:
            print(f"Process with id '{process_id}' deleted successfully.")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error occurred: {str(e)}")

