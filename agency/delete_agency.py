import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def delete_agency(agency_id: int):
    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Execute the DELETE query
        cur.execute("DELETE FROM agencies WHERE agency_id = %s;", (agency_id,))

        # Commit the transaction
        conn.commit()

        # Check if any rows were deleted
        if cur.rowcount == 0:
            raise Exception(f"No agency found with the id '{agency_id}'.")
        else:
            print(f"Agency with id '{agency_id}' deleted successfully.")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error occurred: {str(e)}")

