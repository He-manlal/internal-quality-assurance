import psycopg2
import os
from psycopg2 import sql
from dotenv import load_dotenv
load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")

def create_process(process_name, description):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO processes (process_name,\"Description\",created_at) VALUES (%s, %s, NOW())",
        (process_name, description)
    )
    
    conn.commit()
    cur.close()
    conn.close()
    print("Process created successfully.")

# Example
if __name__ == "__main__":
    create_process("Prepare for Audit", "Collect all documents before audit.")

