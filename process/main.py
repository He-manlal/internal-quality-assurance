from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from create_process import create_process  # Import the function from create_process.py
from delete_process import delete_process  # Import the function from delete_process.py
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize FastAPI app
app = FastAPI()

# Pydantic model for request body validation
class ProcessRequest(BaseModel):
    process_name: str
    description: str

# POST endpoint to create a process
@app.post("/create-process")
async def create_process_endpoint(process: ProcessRequest):
    try:
        create_process(process.process_name, process.description)
        return {"message": "Process created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET endpoint to display all processes
@app.get("/")
async def get_all_processes():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT * FROM processes;")
        rows = cur.fetchall()

        if not rows:
            return {"message": "No processes found."}

        processes = [{"process_id": row[0],"process_name": row[1], "description": row[2], "created_at": row[3]} for row in rows]
        cur.close()
        conn.close()

        return {"processes": processes}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DELETE endpoint to delete a process by ID
@app.delete("/delete-process/{process_id}")
async def delete_process_endpoint(process_id: int):
    try:
        # Call the delete_process function from delete_process.py
        delete_process(process_id)
        return {"message": f"Process with ID {process_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

