import psycopg2
import os
from psycopg2 import sql
from dotenv import load_dotenv
load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")

def create_agency(agency_name, description):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO agencies (agency_name,description,created_at) VALUES (%s, %s, NOW())",
        (agency_name, description)
    )
    
    conn.commit()
    cur.close()
    conn.close()
    print("Agency created successfully.")



