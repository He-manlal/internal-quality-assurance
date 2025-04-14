from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from db import get_db
import requests
import json
router = APIRouter()
import ids_exist  # Corrected to use ids_exist

class AuditCreate(BaseModel):
    agency_id: int
    process_id: int

@router.post("/audit")
def create_audit(audit: AuditCreate):
    conn, cursor = get_db()
    try:
        # Check if process_id exists using ids_exist
        process_id_exists = ids_exist.check_process_id(audit.process_id)
        if not process_id_exists:
            raise HTTPException(status_code=404, detail="Process ID does not exist")
        
        # Check if agency_id exists using ids_exist
        agency_id_exists = ids_exist.check_agency_id(audit.agency_id)
        if not agency_id_exists:
            raise HTTPException(status_code=404, detail="Agency ID does not exist")

        # Insert the audit into the database
        query = """
        INSERT INTO audit (agency_id, process_id, final_status)
        VALUES (%s, %s, 'pending')
        RETURNING audit_id;
        """
        cursor.execute(query, (audit.agency_id, audit.process_id))
        audit_id = cursor.fetchone()[0]
        conn.commit()

        return {"audit_id": audit_id}

    finally:
        cursor.close()
        conn.close()
