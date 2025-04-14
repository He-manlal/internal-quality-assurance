from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from create_agency import create_agency  # Import the function from create_agency.py
from delete_agency import delete_agency  # Import the function from delete_agency.py
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize FastAPI app
app = FastAPI()

# Pydantic model for request body validation
class AgencyRequest(BaseModel):
    agency_name: str
    description: str

# POST endpoint to create a agency
@app.post("/create-agency")
async def create_agency_endpoint(agency: AgencyRequest):
    try:
        create_agency(agency.agency_name, agency.description)
        return {"message": "agency created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET endpoint to display all agencies
@app.get("/")
async def get_all_agencies():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT * FROM agencies;")
        rows = cur.fetchall()

        if not rows:
            return {"message": "No agencies found."}

        agencies = [{"agency_id": row[0], "agency_name": row[1], "description": row[2], "created_at": row[3]} for row in rows]
        cur.close()
        conn.close()

        return {"agencies": agencies}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DELETE endpoint to delete a agency by ID
@app.delete("/delete-agency/{agency_id}")
async def delete_agency_endpoint(agency_id: int):
    try:
        # Call the delete_agency function from delete_agency.py
        delete_agency(agency_id)
        return {"message": f"agency with ID {agency_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

