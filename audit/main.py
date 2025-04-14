from fastapi import FastAPI
from audit import router as audit_router
from audit_step import router as audit_step_router
from dotenv import load_dotenv
import psycopg2
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()


app.include_router(audit_router)
app.include_router(audit_step_router)

# Database connection logic
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    """ Function to get a connection to the database """
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    return conn, cursor


@app.get("/")
async def get_all_audits():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT * FROM audit;")
        rows = cur.fetchall()

        if not rows:
            return {"message": "No audits found."}

        audits = [{"audit_id": row[0],"agency_id": row[1], "process_id": row[2], "final_status": row[3]} for row in rows]
        cur.close()
        conn.close()

        return {"audits": audits}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
